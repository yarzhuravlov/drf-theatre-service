from payments.services.stripe import StripePaymentService
from reservations.models import Reservation


def get_payment_service(provider: str, reservation: Reservation):
    if provider == "stripe":
        return StripePaymentService(reservation)

    raise NotImplementedError(f"No provider for: {provider}")
