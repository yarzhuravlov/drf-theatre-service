from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

reservation_view_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of reservations made by the authenticated user.",
    ),
    create=extend_schema(
        description="Create a new reservation with tickets for the authenticated user.",
    ),
    retrieve=extend_schema(
        description="Retrieve details of a specific reservation by its ID.",
    ),
)
