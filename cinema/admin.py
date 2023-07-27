from django.contrib import admin

from cinema.models import (
    Movie,
    Genre,
    Actor,
    Producer,
    CinemaHall,
    MovieSession,
)


admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Producer)
admin.site.register(CinemaHall)


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ["movie", "show_time", "cinema_hall"]
    ordering = ["movie", "show_time"]
