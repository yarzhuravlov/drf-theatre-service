from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ForeignKey, ManyToManyField

from base.models import CreatedAtBaseModel
from theatre.models import Ticket

User = get_user_model()


class Reservation(CreatedAtBaseModel, models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    tickets = ManyToManyField(Ticket)

    class Meta(CreatedAtBaseModel.Meta):
        default_related_name = "reservations"
