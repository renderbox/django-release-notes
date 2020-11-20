from django.views.generic import TemplateView, DetailView, ListView

from .models import Release

class ReleaseNotesIndexView(TemplateView):
    template_name = "releasenotes/index.html"


class ReleaseNotesListView(ListView):
    """
    All releases for the project
    """
    queryset = Release.objects.filter(project__slug="training-camp")


class ReleaseNotesDetailView(DetailView):
    """
    If a specific release is not provided, default to the current release
    """
    queryset = Release.objects.filter(project__slug="training-camp", state=Release.ReleaseState.CURRENT)