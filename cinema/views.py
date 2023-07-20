import qrcode
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View

from cinema.forms import GuestCreationForm
from cinema.models import (
    Movie,
    MovieSession,
    Order,
    Guest,
    Ticket
)

from django.views.generic import CreateView


class CreateUserView(CreateView):
    model = Guest
    form_class = GuestCreationForm
    success_url = reverse_lazy("cinema:login")

    template_name = "registration/guest_register.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class IndexView(generic.ListView):
    model = Movie
    queryset = Movie.objects.prefetch_related(
        "actors"
    ).prefetch_related(
        "producers"
    ).order_by(
        "-release_date"
    )

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        queryset = Movie.objects.prefetch_related(
            "actors"
        ).prefetch_related(
            "producers"
        ).order_by(
            "-release_date"
        )

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset


class MovieDetailView(generic.DetailView):
    model = Movie


class SessionDetailView(generic.DetailView):
    model = MovieSession
    template_name = "cinema/movie_session_detail.html"

    @staticmethod
    def post(request, **kwargs):
        chosen_seats = request.POST.getlist("chosen_seats")
        movie_session_id = request.POST.get('movie_session_id')

        if movie_session_id:
            movie_session = MovieSession.objects.get(id=movie_session_id)
        else:
            movie_session = None

        create_order_with_tickets(
            chosen_seats=chosen_seats,
            movie_session=movie_session,
            request=request
        )

        return redirect("cinema:ticket-listview")

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
                1 if (row, col) in seats_taken else 0
                for col in range(1, cols + 1)
             ]
            for row in range(1, rows + 1)
        ]

        context["seat_matrix"] = seat_matrix

        return context


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = "cinema/order.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(order__guest=self.request.user)
        return queryset


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect('/')


@transaction.atomic
def create_order_with_tickets(
        chosen_seats: list,
        movie_session: MovieSession,
        request
) -> None:
    order = Order.objects.create(guest=request.user)
    for item in chosen_seats:
        item = item.split(",")
        row = int(item[0])
        seat = int(item[-1])

        ticket = Ticket.objects.create(
            row=row,
            seat=seat,
            order=order,
            movie_session=movie_session
        )
        create_qrcode(ticket)
        ticket.qr_code = f"media/{ticket.id}.png"
        ticket.save()


def create_qrcode(ticket: Ticket):
    data = (
        f"{ticket.id}_"
        f"{ticket.row}_"
        f"{ticket.seat}_"
        f"{ticket.order.id}_"
        f"{ticket.movie_session.id}"
    )
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save(f"static/media/{ticket.id}.png")
