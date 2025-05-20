from datetime import timedelta, datetime, timezone as datetime_timezone

import stripe
from django.conf import settings
from django.utils import timezone

from .base import AbstractPaymentService
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService(AbstractPaymentService):
    def check_existing_payment(self):
        return Payment.objects.filter(
            reservation=self.reservation,
            provider="stripe",
            status=Payment.Statuses.PENDING,
            expires_at__gt=timezone.now(),
        ).first()

    def create_session(self, currency, expiration_minutes):
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": f"Reservation #{self.reservation.id}",
                        },
                        "unit_amount": self.reservation.total_price,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.FRONTEND_SUCCESS_URL,
            cancel_url=settings.FRONTEND_CANCEL_URL,
            metadata={"reservation_id": self.reservation.id},
            expires_at=int(
                (
                    timezone.now() + timedelta(minutes=expiration_minutes)
                ).timestamp()
            ),
            customer_email=self.reservation.user.email,
        )
        return session

    def create_payment(self, session):
        Payment.objects.create(
            reservation=self.reservation,
            provider="stripe",
            status="pending",
            external_id=session.id,
            checkout_url=session.url,
            expires_at=datetime.fromtimestamp(
                session.expires_at,
                tz=datetime_timezone.utc,
            ),
        )

    def retrieve_or_create_checkout_session(self) -> str:
        expiration_minutes = settings.PAYMENT_SESSION_EXPIRATION_MINUTES
        currency = settings.PAYMENT_CURRENCY

        existing_payment = self.check_existing_payment()

        if existing_payment:
            return existing_payment.checkout_url

        session = self.create_session(currency, expiration_minutes)

        self.create_payment(session)

        return session.url

    def handle_webhook(self, payload: dict, sig_header: str) -> None:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            payment = Payment.objects.get(external_id=session["id"])
            # TODO: check session with stripe API
            payment.status = Payment.Statuses.CONFIRMED
            payment.save()
