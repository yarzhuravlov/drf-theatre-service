from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    TheatreHall,
    Ticket,
    Zone,
    ZonePrice,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    actors = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name"]


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["id", "name", "theatre_hall", "rows", "seats_in_row"]


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time", "zones"]
        read_only_fields = ["zones"]


class PerformanceListSerializer(PerformanceSerializer):
    play = PlayListSerializer(read_only=True)
    theatre_hall = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    available_tickets = serializers.IntegerField()

    class Meta:
        model = Performance
        fields = [
            "id",
            "play",
            "theatre_hall",
            "show_time",
            "available_tickets",
        ]


class PerformanceInPlayListSerializer(PerformanceListSerializer):
    class Meta(PerformanceListSerializer.Meta):
        fields = ["id", "theatre_hall", "show_time", "available_tickets"]


class PlayRetrieveSerializer(PlayListSerializer):
    future_performances = PerformanceInPlayListSerializer(many=True)

    class Meta(PlayListSerializer.Meta):
        fields = PlayListSerializer.Meta.fields + ["future_performances"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "zone", "row", "seat"]


class ZoneInPerformanceDetailSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer()

    class Meta:
        model = ZonePrice
        fields = ["id", "zone", "ticket_price"]


class PerformanceDetailSerializer(PerformanceListSerializer):
    zone_prices = ZoneInPerformanceDetailSerializer(many=True)
    tickets = TicketSerializer(many=True)

    class Meta(PerformanceListSerializer.Meta):
        fields = PerformanceListSerializer.Meta.fields + [
            "tickets",
            "zone_prices",
        ]
