from django.urls import path

from cinema.views import IndexView, MovieDetailView, SessionDetailView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("movie/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("movie/session/<int:pk>/", SessionDetailView.as_view(), name="movie-session-detail")
]

app_name = "cinema"
