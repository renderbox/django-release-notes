import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import Permission

from autoslug import AutoSlugField


class CreateUpdateModelBase(models.Model):
    '''
    This is a shared models base that provides created & updated timestamp fields
    '''
    created = models.DateTimeField("date created", auto_now_add=True)
    updated = models.DateTimeField("last updated", auto_now=True)

    class Meta:
        abstract = True

class Project(CreateUpdateModelBase):
    """
    The Project the release notes are for.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    site = models.ForeignKey(Site, verbose_name=_("Site"), on_delete=models.CASCADE, default=settings.SITE_ID, related_name="projects")
    slug = AutoSlugField(populate_from='name', unique_with='site__id')

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


class Release(CreateUpdateModelBase):
    """
    This is the actual release
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='name', unique_with='site__id')
    major = models.IntegerField(_("Major"))
    minor = models.IntegerField(_("Minor"))
    path = models.CharField(_("Patch"), max_length=50)

    class Meta:
        verbose_name = _("Release")
        verbose_name_plural = _("Releases")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("release_detail", kwargs={"pk": self.pk})


class Note(CreateUpdateModelBase):
    """
    Note attached to the Release
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    release = models.ForeignKey(Release, verbose_name=_("release"), on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, verbose_name=_("Permission"), on_delete=models.CASCADE, related_name="permafrost_role", blank=True, null=True)
    text = models.TextField(_("Text"))
    order = models.IntegerField(_("Order"))

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Note_detail", kwargs={"pk": self.pk})
