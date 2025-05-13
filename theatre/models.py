from typing import Iterable
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)

    class Meta:
        default_related_name = "plays"

    def __str__(self) -> str:
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=255)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.PROTECT)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    class Meta:
        default_related_name = "zones"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "theatre_hall"],
                name="unique_name_theatre_hall",
            )
        ]

    def __str__(self) -> str:
        return f"{self.theatre_hall.name} - {self.name}"


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.PROTECT)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.PROTECT)
    show_time = models.DateTimeField()
    zones = models.ManyToManyField(Zone, through="ZonePrice")

    class Meta:
        default_related_name = "performances"

    def __str__(self) -> str:
        return (
            f"{self.play.title} in {self.theatre_hall.name} ({self.show_time})"
        )


class ZonePrice(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    performance = models.ForeignKey(Performance, on_delete=models.PROTECT)
    ticket_price = models.PositiveBigIntegerField()

    class Meta:
        default_related_name = "zone_prices"
        constraints = [
            models.UniqueConstraint(
                fields=["zone", "performance"],
                name="unique_zone_performance",
            )
        ]

    def __str__(self) -> str:
        return f"{self.performance} - {self.zone.name}"


class Ticket(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.PROTECT)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        default_related_name = "tickets"
        constraints = [
            models.UniqueConstraint(
                fields=["performance", "zone", "row", "seat"],
                name="unique_performance_zone_row_seat",
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.performance} - {self.zone.name} ({self.row}, {self.seat})"
        )

    @staticmethod
    def validate_seat(
        row: int,
        rows: int,
        seat: int,
        seats_in_row: int,
        error_to_raise: type[Exception],
    ):
        if not (1 <= seat <= seats_in_row):
            raise error_to_raise(
                {
                    "seat": (
                        f"seat must be in range "
                        f"[1, {seats_in_row}] not {seat}"
                    )
                }
            )

        if not (1 <= row <= rows):
            raise error_to_raise(
                {"seat": (f"seat must be in range " f"[1, {rows}] not {row}")}
            )

    @staticmethod
    def validate_zone(
        performance: Performance, zone: Zone, error_to_raise: type[Exception]
    ):
        if not Performance.objects.filter(
            id=performance.id,
            zones=zone,
        ).exists():
            raise error_to_raise(
                {"zone": "This zone is not available for this performance"}
            )

    def clean(self) -> None:
        Ticket.validate_zone(
            self.performance,
            self.zone,
            ValueError,
        )
        Ticket.validate_seat(
            self.row,
            self.zone.rows,
            self.seat,
            self.zone.seats_in_row,
            ValueError,
        )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)
