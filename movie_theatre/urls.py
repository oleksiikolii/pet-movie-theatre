from django.contrib import admin
from django.urls import path, include

import cinema

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path("", include("cinema.urls", namespace="cinema"))
]
