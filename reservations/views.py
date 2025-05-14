from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from base.mixins import BaseViewSetMixin
from reservations.models import Reservation
from reservations.serializers import (
    ReservationCreateSerializer,
    ReservationListSerializer,
    ReservationSerializer,
)


class ReservationViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    action_serializers = {
        "create": ReservationCreateSerializer,
        "list": ReservationListSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(user=self.request.user)
