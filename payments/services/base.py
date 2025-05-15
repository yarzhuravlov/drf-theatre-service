from abc import ABC, abstractmethod

from reservations.models import Reservation


class AbstractPaymentService(ABC):
    def __init__(self, reservation: Reservation = None):
        self.reservation = reservation

    @abstractmethod
    def create_checkout_session(self) -> str:
        """Returns a redirect URL to the payment provider"""
        pass

    @abstractmethod
    def handle_webhook(self, payload: dict, sig_header: str) -> None:
        """Handle provider webhook event"""
        pass
