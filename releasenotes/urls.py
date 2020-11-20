from django.urls import path

from releasenotes import views

app_name = "releasenotes"

urlpatterns = [
    path("", views.ReleaseNotesIndexView.as_view(), name="index"),
    path("<slug:slug>/", views.ReleaseNotesProjectView.as_view(), name="details"),
]
