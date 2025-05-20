from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)

from theatre.serializers import (
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ActorSerializer,
    GenreSerializer,
)

play_view_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of plays with their genres and actors.",
    ),
    retrieve=extend_schema(
        description="Retrieve detailed information about a specific play, including its future performances.",
    ),
)

performance_view_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of performances with available tickets and related play details.",
        responses=PerformanceListSerializer,
    ),
    retrieve=extend_schema(
        description="Retrieve detailed information about a specific performance, including zone prices and tickets.",
        responses=PerformanceDetailSerializer,
    ),
)

actor_view_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of actors with search functionality.",
        responses=ActorSerializer,
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search actors by first or last name.",
                required=False,
                type=str,
            )
        ],
    ),
)

genre_view_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of genres with search functionality.",
        responses=GenreSerializer,
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search genres by name.",
                required=False,
                type=str,
            )
        ],
    ),
)
