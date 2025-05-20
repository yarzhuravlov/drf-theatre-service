from django.db import models

from base.models import TimestampedBaseModel
from reservations.models import Reservation


class Payment(TimestampedBaseModel, models.Model):
    class Statuses(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        EXPIRED = "expired"
        CANCELLED = "cancelled"

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.PROTECT,
        related_name="payment",
    )
    provider = models.CharField(max_length=63)
    status = models.CharField(max_length=20, choices=Statuses.choices)
    checkout_url = models.TextField()
    external_id = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["reservation"])]
