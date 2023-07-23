import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.test import TestCase
from django.urls import reverse

from cinema.models import Movie, MovieSession, CinemaHall, Ticket, Order
from cinema.views import IndexView, SessionDetailView, TicketListView


class TestIndexView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="StrongPassword123"
        )
        self.client.force_login(self.user)

    def test_index_view_context(self):
        movie = Movie.objects.create(
            title="Test Movie Title",
            description="Some text to hold this place",
            release_date="2000-01-01",
            rating=55,
            country="USA",
            poster_link="link/to/img.png"
        )
        movie2 = Movie.objects.create(
            title="Test Movie Title 2",
            description="Some text to hold this place 2",
            release_date="2000-01-02",
            rating=56,
            country="USA",
            poster_link="link/to/img.png"
        )
        response = self.client.get(reverse("cinema:index"))
        movies = Movie.objects.all()
        self.assertEqual(
            list(response.context["movie_list"]),
            list(movies)
        )


class SessionDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="StrongPassword123"
        )
        self.client.force_login(self.user)
        self.movie_session = MovieSession.objects.create(
            movie=Movie.objects.create(
                title="The Shawshank Redemption",
                release_date="2000-01-01",
                rating=55
            ),
            show_time=datetime.datetime.fromisoformat("2023-07-21 20:00:00"),
            cinema_hall=CinemaHall.objects.create(
                name="Theater 1",
                rows=5,
                seats_in_row=5
            ),
        )

    def test_post(self):
        view = SessionDetailView()
        request = self.client.post(
            reverse(
                "cinema:movie-session-detail",
                kwargs={"pk": self.movie_session.pk}),
            data={
                "chosen_seats": ["1,1", "1,2"],
                "movie_session_id": 1
            }
        )

        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse("cinema:ticket-listview"))


class TicketListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="StrongPassword123"
        )
        self.movie_session = MovieSession.objects.create(
            movie=Movie.objects.create(
                title="The Shawshank Redemption",
                release_date="2000-01-01",
                rating=55
            ),
            show_time=datetime.datetime.fromisoformat("2023-07-21 20:00:00"),
            cinema_hall=CinemaHall.objects.create(
                name="Theater 1",
                rows=5,
                seats_in_row=5
            ),
        )
        self.ticket = Ticket.objects.create(
            movie_session=self.movie_session,
            seat="1",
            row="1",
            order=Order.objects.create(guest=self.user)
        )

    def test_get_queryset(self):
        view = TicketListView()
        view.request = self.client.get(reverse("cinema:ticket-listview"))
        view.request.user = self.user

        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0], self.ticket)

