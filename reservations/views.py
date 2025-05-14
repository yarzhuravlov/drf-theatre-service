from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from base.mixins import BaseViewSetMixin
from reservations.models import Reservation
from reservations.serializers import (
    ReservationCreateSerializer,
    ReservationListSerializer,
    ReservationSerializer,
)
from reservations.services import ReservationService


class ReservationViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    reservations_service = ReservationService("stripe")

    action_serializers = {
        "create": ReservationCreateSerializer,
        "list": ReservationListSerializer,
    }

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.reservations_service.create_payment_for_reservation(
            serializer.instance
        )

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(user=self.request.user)
