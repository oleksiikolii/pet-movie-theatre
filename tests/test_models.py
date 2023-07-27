import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from cinema.models import (
    Genre,
    Producer,
    Actor,
    Movie,
    CinemaHall,
    MovieSession,
    Order,
    Ticket,
)


class TestGenre(TestCase):
    def test_genre_create(self):
        genre = Genre.objects.create(name="Art House")
        return self.assertEqual(str(genre), "Art House")


class TestActor(TestCase):
    def test_actor_create(self):
        actor = Actor.objects.create(full_name="Morgan Freeman")
        return self.assertEqual(str(actor), "Morgan Freeman")


class TestProducer(TestCase):
    def test_producer_create(self):
        producer = Producer.objects.create(full_name="James Cameron")
        return self.assertEqual(str(producer), "James Cameron")


class TestMovie(TestCase):
    def setUp(self) -> None:
        james_cameron = Producer.objects.create(full_name="James Cameron")
        christopher_nolan = Producer.objects.create(
            full_name="Christopher Nolan"
        )

        action = Genre.objects.create(name="Action")
        drama = Genre.objects.create(name="Drama")

        movie = Movie.objects.create(
            title="Test Movie Title",
            description="Some text to hold this place",
            release_date="2000-01-21",
            rating=55,
            country="USA",
            poster_link="link/to/img.png",
        )
        movie.producers.add(james_cameron, christopher_nolan)
        movie.genres.add(drama, action)

        self.movie = movie

        self.hall = CinemaHall.objects.create(
            name="test hall", rows=10, seats_in_row=10
        )
        self.session1 = MovieSession.objects.create(
            movie=movie,
            cinema_hall=self.hall,
            show_time=datetime.datetime.fromisoformat("2023-07-21 19:00"),
        )
        self.session2 = MovieSession.objects.create(
            movie=movie,
            cinema_hall=self.hall,
            show_time=datetime.datetime.fromisoformat("2023-07-22 21:00"),
        )
        self.user = get_user_model().objects.create_user(
            username="TestUser", password="StrongPassword123"
        )

    def test_user(self):
        user = self.user
        test_user = get_user_model().objects.get(id=1)
        self.assertEqual(user.username, test_user.username)

    def test_movie_repr(self):
        movie = self.movie
        return self.assertEqual(str(movie), "Test Movie Title")

    def test_get_sessions(self):
        movie = self.movie

        today_session = movie.get_today_movie_sessions()
        tomorrow_session = movie.get_tomorrow_movie_sessions()

        self.assertEqual(today_session.first().show_time.day, 21)
        self.assertEqual(tomorrow_session.first().show_time.day, 22)

    def test_get_rating(self):
        self.assertEqual(self.movie.get_rating(), 5.5)

    def test_movie_session(self):
        session = self.session1
        self.assertEqual(str(session), "Fri 21 Jul 2023, 19:00")
        self.assertEqual(session.get_time(), "19:00")

    def test_cinema_hall(self):
        hall = self.hall
        self.assertEqual(hall.capacity, 10 * 10)
        self.assertEqual(str(hall), "test hall")

    def test_ticket(self):
        order = Order.objects.create(guest=self.user)
        ticket = Ticket.objects.create(
            row=1, seat=1, order=order, movie_session=self.session1
        )
        self.assertEqual(
            str(ticket),
            "Test Movie Title 2023-07-21 19:00:00 (row: 1, seat: 1)",
        )
