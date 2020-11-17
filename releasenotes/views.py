from django.views.generic import TemplateView

class ReleaseNotesIndexView(TemplateView):
    template_name = "releasenotes/index.html"
