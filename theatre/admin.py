from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    TheatreHall,
    Zone,
    ZonePrice,
)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    pass


class ZoneInline(admin.StackedInline):
    model = Zone


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    inlines = [ZoneInline]


class ZonePriceInline(admin.StackedInline):
    model = ZonePrice


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    inlines = [ZonePriceInline]
