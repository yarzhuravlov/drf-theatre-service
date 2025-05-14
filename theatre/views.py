from django.db.models import Prefetch, QuerySet
from django.utils.timezone import now
from rest_framework import filters, generics, viewsets

from base.mixins import BaseViewSetMixin
from theatre.filters import PerformanceFilter
from theatre.models import Actor, Genre, Performance, Play
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PerformanceDetailSerializer,
    PerformanceListSerializer,
    PerformanceSerializer,
    PlayListSerializer,
    PlayRetrieveSerializer,
    PlaySerializer,
)


class PlayViewSet(
    BaseViewSetMixin,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    viewsets.ViewSet,
):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer

    action_serializers = {
        "list": PlayListSerializer,
        "retrieve": PlayRetrieveSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "retrieve":
            print(self.args, self.kwargs)
            queryset = queryset.prefetch_related(
                Prefetch(
                    "performances",
                    queryset=Performance.annotate_with_available_tickets(
                        Performance.objects.filter(
                            play__id=int(self.kwargs["pk"]),
                            show_time__gt=now(),
                        ),
                    )
                    .distinct()
                    .prefetch_related(
                        "play__actors",
                        "play__genres",
                    ),
                    to_attr="future_performances",
                )
            )

        return queryset


class PerformanceViewSet(
    BaseViewSetMixin,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    viewsets.ViewSet,
):
    queryset = Performance.objects.select_related(
        "theatre_hall",
    )
    serializer_class = PerformanceSerializer
    filterset_class = PerformanceFilter

    action_serializers = {
        "list": PerformanceListSerializer,
        "retrieve": PerformanceDetailSerializer,
    }

    def get_queryset(self) -> QuerySet[Performance]:
        queryset = self.queryset

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "zone_prices__zone",
                "zones",
            )

        if self.action in {"list", "retrieve"}:
            queryset = (
                Performance.annotate_with_available_tickets(queryset)
                .distinct()
                .prefetch_related(
                    "play__actors",
                    "play__genres",
                )
            )

        return queryset


class ActorViewSet(generics.ListAPIView, viewsets.ViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name"]


class GenreViewSet(generics.ListAPIView, viewsets.ViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
