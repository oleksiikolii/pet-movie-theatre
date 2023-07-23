from django.contrib import admin

from cinema.models import (
    Movie,
    Genre,
    Actor,
    Producer,
    CinemaHall,
    MovieSession
)


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    pass


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    pass


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    pass


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ["movie", "show_time", "cinema_hall"]
    ordering = ["movie", "show_time"]
