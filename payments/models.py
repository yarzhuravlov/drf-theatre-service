from django.db import models

from base.models import CreatedAtBaseModel
from reservations.models import Reservation


class Payment(CreatedAtBaseModel, models.Model):
    class Statuses(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        EXPIRED = "expired"
        CANCELLED = "cancelled"

    reservation = models.OneToOneField(Reservation, on_delete=models.PROTECT)
    provider = models.CharField(max_length=63)
    status = models.CharField(max_length=20, choices=Statuses.choices)
    checkout_url = models.TextField()
    external_id = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["reservation"])]
