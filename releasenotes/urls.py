from django.urls import path

from releasenotes import views

app_name = "releasenotes"

urlpatterns = [
    path("", views.ReleaseNotesIndexView.as_view(), name="index"),
    path("<slug:project_slug>/", views.ReleaseNotesProjectView.as_view(), name="project-details"),
    path("<slug:project_slug>/<str:release_slug>/", views.ReleaseNotesDetailView.as_view(), name="release-details"),
]
