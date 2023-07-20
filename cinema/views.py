from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from cinema.models import Movie, MovieSession


# Create your views here.
class IndexView(generic.ListView):
    model = Movie
    queryset = Movie.objects.prefetch_related("actors").prefetch_related("producers").order_by("-release_date")


class MovieDetailView(generic.DetailView):
    model = Movie


class SessionDetailView(generic.DetailView):
    model = MovieSession
    template_name = "cinema/movie_session_detail.html"

    def post(self, request, **kwargs):
        checked_checkboxes = request.POST

        # Do something with the checked checkboxes
        print(checked_checkboxes)
        return HttpResponse("success")

    def get_context_data(self, **kwargs):
        context = super(SessionDetailView, self).get_context_data(**kwargs)

        movie_session = context.get("moviesession")
        rows, cols = movie_session.cinema_hall.rows, movie_session.cinema_hall.seats_in_row
        tickets = list(movie_session.tickets.all())
        seats_taken = [
            (ticket.row, ticket.seat)
            for ticket in tickets
        ]
        seat_matrix = [
            [
                1 if (col, row) in seats_taken else 0
                for col in range(1, cols + 1)
             ]
            for row in range(1, rows + 1)
        ]

        context["seat_matrix"] = seat_matrix

        return context

