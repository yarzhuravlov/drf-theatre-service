from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

create_checkout_session_view_schema = extend_schema_view(
    post=extend_schema(
        description="Create or retrieve a Stripe checkout session for a reservation.",
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "checkout_url": {
                            "type": "string",
                            "description": "URL to redirect the user to the Stripe checkout session.",
                        }
                    },
                },
                description="Checkout session created successfully.",
            ),
            404: OpenApiResponse(
                description="Reservation not found.",
            ),
        },
    )
)

stripe_webhook_view_schema = extend_schema_view(
    post=extend_schema(
        description="Handle Stripe webhook events.",
        request=None,
    )
)
