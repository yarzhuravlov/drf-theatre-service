import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone as datetime_timezone, timedelta
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase

from payments.models import Payment
from reservations.models import Reservation
from theatre.models import (
    Play,
    Performance,
    Zone,
    Ticket,
    TheatreHall,
    ZonePrice,
)

User = get_user_model()


class ReservationViewSetTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )

        # Create another user for authorization tests
        self.another_user = User.objects.create_user(
            email="another@example.com",
            password="testpassword",
        )

        # Create play and performance
        self.play = Play.objects.create(
            title="Test Play", description="Test Description"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Theatre Hall",
        )
        self.performance = Performance.objects.create(
            play=self.play,
            show_time="2025-05-15T19:00:00Z",
            theatre_hall=self.theatre_hall,
        )

        # Create zone and zone price
        self.zone = Zone.objects.create(
            name="Test Zone",
            rows=10,
            seats_in_row=20,
            theatre_hall=self.theatre_hall,
        )
        self.zone_price = ZonePrice.objects.create(
            zone=self.zone, performance=self.performance, ticket_price=1000
        )

        # Create ticket
        self.ticket = Ticket.objects.create(
            seat=5,
            row=3,
            performance=self.performance,
            zone=self.zone,
        )

        # Create reservation
        self.reservation = Reservation.objects.create(user=self.user)
        self.reservation.tickets.add(self.ticket)

        # Setup API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Set up URLs
        self.list_url = reverse("v1:reservations:reservation-list")
        self.detail_url = reverse(
            "v1:reservations:reservation-detail", args=[self.reservation.id]
        )

        # Mock payment service
        self.payment_service_mock = MagicMock()
        self.payment_service_mock.create_checkout_session.return_value = (
            "https://test-checkout-url.com"
        )

    def test_get_reservations_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.reservation.id)

        # Check that tickets are included in the response
        self.assertEqual(len(response.data[0]["tickets"]), 1)
        self.assertEqual(
            response.data[0]["tickets"][0]["seat"], self.ticket.seat
        )
        self.assertEqual(
            response.data[0]["tickets"][0]["row"], self.ticket.row
        )
        self.assertEqual(
            response.data[0]["tickets"][0]["zone"], self.zone.name
        )

    @patch(
        "reservations.views.ReservationService.create_payment_for_reservation"
    )
    def test_create_reservation(self, mock_service_class):
        mock_service_class.return_value = self.payment_service_mock

        # Create new tickets data
        new_ticket_data = {
            "tickets": [
                {
                    "seat": 10,
                    "row": 5,
                    "performance": self.performance.id,
                    "zone": self.zone.id,
                    "price": 1500,
                }
            ]
        }

        response = self.client.post(
            self.list_url,
            data=json.dumps(new_ticket_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get("id"))

        # Verify reservation was created properly
        new_reservation = Reservation.objects.get(id=response.data.get("id"))
        self.assertEqual(new_reservation.user, self.user)
        self.assertEqual(new_reservation.tickets.count(), 1)

        # Verify payment service was called
        mock_service_class.assert_called_once_with(new_reservation)

    def test_prevent_reservation_with_pending_payment(
        self,
    ):
        # Create a reservation with a pending payment
        reservation_with_pending = Reservation.objects.create(user=self.user)
        Payment.objects.create(
            reservation=reservation_with_pending,
            provider="stripe",
            status=Payment.Statuses.PENDING,
            external_id="test_external_id",
            checkout_url="https://test-checkout-url.com",
            expires_at=datetime.fromtimestamp(
                int(
                    (
                        timezone.now()
                        + timedelta(
                            minutes=settings.PAYMENT_SESSION_EXPIRATION_MINUTES
                        )
                    ).timestamp()
                ),
                tz=datetime_timezone.utc,
            ),
        )

        # Try to create another reservation
        new_ticket_data = {
            "tickets": [
                {
                    "seat": 10,
                    "row": 5,
                    "performance": self.performance.id,
                    "zone": self.zone.id,
                    "price": 1500,
                }
            ]
        }

        response = self.client.post(
            self.list_url,
            data=json.dumps(new_ticket_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("pending payment", str(response.data))
