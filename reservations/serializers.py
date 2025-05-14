from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from payments.models import Payment
from reservations.models import Reservation
from theatre.models import Ticket, Performance
from theatre.serializers import (
    TicketSerializer,
)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ["id", "user", "tickets"]


class ReservationCreateSerializer(ReservationSerializer):
    class Meta(ReservationSerializer.Meta):
        fields = ["tickets"]

    def validate(self, attrs):
        tickets_data = attrs["tickets"]

        if len(tickets_data) > 10:
            raise serializers.ValidationError(
                "You cannot add more than 10 tickets to one reservation"
            )

        for ticket_data in tickets_data:
            Ticket.validate_zone(
                ticket_data["performance"],
                ticket_data["zone"],
                serializers.ValidationError,
            )

            Ticket.validate_seat(
                ticket_data["row"],
                ticket_data["zone"].rows,
                ticket_data["seat"],
                ticket_data["zone"].seats_in_row,
                serializers.ValidationError,
            )

        if Reservation.objects.filter(
            user=self.context["request"].user,
            payment__status=Payment.Statuses.PENDING,
        ).exists():
            raise serializers.ValidationError(
                "You can't create reservation while "
                "you have pending payment on other reservation"
            )

        return attrs

    def create(self, validated_data: dict):
        tickets_data = validated_data.pop("tickets")
        request = self.context.get("request")
        validated_data["user"] = request.user

        with transaction.atomic():
            reservation = Reservation.objects.create(
                **validated_data,
            )

            tickets = [
                Ticket.objects.create(**ticket_data)
                for ticket_data in tickets_data
            ]

            reservation.tickets.add(*tickets)

            return reservation


class PerformanceInReservationTicketSerializer(serializers.ModelSerializer):
    play = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Performance
        fields = ["id", "play"]


class TicketInReservationSerializer(serializers.ModelSerializer):
    performance = PerformanceInReservationTicketSerializer(read_only=True)
    zone = SlugRelatedField("name", read_only=True)

    class Meta:
        model = Ticket
        fields = ["seat", "row", "performance", "zone", "price"]


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketInReservationSerializer(many=True)
