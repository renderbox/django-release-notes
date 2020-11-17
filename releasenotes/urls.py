from django.urls import path

from releasenotes import views

urlpatterns = [
    path("", views.ReleaseNotesIndexView.as_view(), name="releasenotes-index"),
]
