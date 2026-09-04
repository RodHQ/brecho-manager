"""URL configuration for brecho_manager."""

from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
]
