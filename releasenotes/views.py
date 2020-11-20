from django.views.generic import TemplateView, DetailView, ListView

from .models import Project, Release

class ReleaseNotesIndexView(ListView):
    template_name = "releasenotes/index.html"
    model = Project


class ReleaseNotesProjectView(DetailView):
    """
    If a specific release is not provided, default to the current release
    """
    model = Project
    slug_url_kwarg = "project_slug"


class ReleaseNotesDetailView(DetailView):
    """
    If a specific release is not provided, default to the current release
    """
    model = Release
    slug_url_kwarg = "release_slug"
