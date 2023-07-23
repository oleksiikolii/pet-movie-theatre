from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Guest(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    full_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.full_name


class Producer(models.Model):
    full_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.full_name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.IntegerField()
    country = models.CharField(max_length=255)
    producers = models.ManyToManyField(Producer, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    genres = models.ManyToManyField(Genre, related_name="movies")
    poster_link = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.title

    def get_today_movie_sessions(self):
        return MovieSession.objects.filter(
            movie=self,
            show_time__day=21,
            # Dates are hard coded due to showcase nature of this site
        )   # We can easily swap it with datetime.date.today().day

    def get_tomorrow_movie_sessions(self):
        query = MovieSession.objects.select_related("movie")
        return query.filter(movie=self, show_time__day=22)

    def get_rating(self):
        return self.rating / 10


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    movie = models.ForeignKey(
        Movie,
        related_name="sessions",
        on_delete=models.CASCADE
    )
    cinema_hall = models.ForeignKey(
        CinemaHall, related_name="sessions", on_delete=models.CASCADE
    )
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["show_time"]

    def __str__(self) -> str:
        return self.show_time.strftime("%a %d %b %Y, %H:%M")

    def get_time(self) -> str:
        return self.show_time.strftime("%H:%M")


class Order(models.Model):
    guest = models.ForeignKey(
        get_user_model(), related_name="orders", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    qr_code = models.CharField(max_length=255, blank=True)
    order = models.ForeignKey(
        Order,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    movie_session = models.ForeignKey(
        MovieSession, related_name="tickets", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["movie_session", "seat", "row"], name="unique_tickets"
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        if not 1 <= self.row <= self.movie_session.cinema_hall.rows:
            raise ValidationError(
                {
                    "row": "row number must be in available range:"
                    " (1, rows): "
                    f"(1, {self.movie_session.cinema_hall.rows})"
                }
            )

        if not 1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": "seat number must be in available range:"
                    " (1, seats_in_row):"
                    f" (1, {self.movie_session.cinema_hall.seats_in_row})"
                }
            )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: bool = None,
        update_fields: bool = None,
    ) -> callable:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
