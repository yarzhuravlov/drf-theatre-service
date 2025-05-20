from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.services.factory import get_payment_service
from payments.services.stripe import StripePaymentService
from reservations.models import Reservation


@extend_schema_view(
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
class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(
            id=reservation_id,
            user=request.user,
        )
        service = get_payment_service("stripe", reservation)
        url = service.retrieve_or_create_checkout_session()

        return Response({"checkout_url": url})


@method_decorator(csrf_exempt, name="dispatch")
@extend_schema_view(
    post=extend_schema(
        description="Handle Stripe webhook events.",
        request=None,
    )
)
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        service = StripePaymentService()
        service.handle_webhook(payload, sig_header)
        return Response(status=200)
