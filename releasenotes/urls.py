from django.urls import path

from releasenotes import views

app_name = "releasenotes"

urlpatterns = [
    path("", views.ReleaseNotesIndexView.as_view(), name="index"),
    path("releases/", views.ReleaseNotesListView.as_view(), name="list"),
    path("release/", views.ReleaseNotesDetailView.as_view(), name="details"),
]
