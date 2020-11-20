from django.views.generic import TemplateView, DetailView

from .models import Project

class ReleaseNotesIndexView(TemplateView):
    template_name = "releasenotes/index.html"


class ReleaseNotesProjectView(DetailView):
    """
    If a specific release is not provided, default to the current release
    """
    model = Project
