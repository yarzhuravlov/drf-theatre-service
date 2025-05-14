from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.services.factory import get_payment_service
from payments.services.stripe import StripePaymentService
from reservations.models import Reservation


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(
            id=reservation_id,
            user=request.user,
        )
        service = get_payment_service("stripe", reservation)
        url = service.create_checkout_session()

        return Response({"checkout_url": url})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        service = StripePaymentService()
        service.handle_webhook(payload, sig_header)
        return Response(status=200)
