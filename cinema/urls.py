from django.contrib.auth.views import LoginView
from django.urls import path

from cinema.views import IndexView, MovieDetailView, SessionDetailView, CreateUserView, TicketListView, LogoutView, \
    render_movie_sessions

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("render_sessions/", render_movie_sessions),
    path(
        "accounts/login/",
        LoginView.as_view(),
        name="login"
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(),
        name="logout"
    ),
    path(
        "accounts/register/",
        CreateUserView.as_view(),
        name="register"
    ),
    path("movie/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("movie/session/<int:pk>/", SessionDetailView.as_view(), name="movie-session-detail"),
    path("orders/", TicketListView.as_view(), name="ticket-listview")
]

app_name = "cinema"
