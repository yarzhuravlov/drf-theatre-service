from django.db.models import F, Count, QuerySet, Sum
from rest_framework import viewsets

from base.mixins import BaseViewSetMixin
from theatre.filters import PerformanceFilter
from theatre.models import Performance, Play
from theatre.serializers import (
    PerformanceListSerializer,
    PerformanceSerializer,
    PlayListSerializer,
    PlaySerializer,
)


class PlayViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer

    action_serializers = {
        "list": PlayListSerializer,
    }


class PerformanceViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        "theatre_hall",
    )
    serializer_class = PerformanceSerializer
    filterset_class = PerformanceFilter

    action_serializers = {
        "list": PerformanceListSerializer,
    }

    def get_queryset(self) -> QuerySet[Performance]:
        queryset = self.queryset

        if self.action == "list":
            queryset = (
                queryset.annotate(
                    tickets_count=Sum(
                        F("zone_prices__zone__rows")
                        * F("zone_prices__zone__seats_in_row"),
                        distinct=True,
                    ),
                    tickets_bought=Count("tickets", distinct=True),
                )
                .annotate(
                    available_tickets=F("tickets_count") - F("tickets_bought"),
                )
                .distinct()
                .prefetch_related(
                    "play__actors",
                    "play__genres",
                )
            )

        return queryset
