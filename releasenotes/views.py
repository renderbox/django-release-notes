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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['new_features'] = [ note for note in context['object'].notes.all() if note.note_type == note.NoteType.NEW_FEATURE]
        context['bug_fixes'] = [ note for note in context['object'].notes.all() if note.note_type == note.NoteType.BUG_FIX]
        context['known_issues'] = [ note for note in context['object'].notes.all() if note.note_type == note.NoteType.KNOWN_ISSUES]

        return context