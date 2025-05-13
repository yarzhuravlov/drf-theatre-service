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
