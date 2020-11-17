import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import Permission
from django.utils.text import slugify


###############
# CHOICES
###############

class NoteType(models.IntegerChoices):
    NEW_FEATURE = 0, _("New Feature")
    BUG_FIX = 10, _("Bug Fix")


###############
# BASE
###############

class CreateUpdateModelBase(models.Model):
    '''
    This is a shared models base that provides created & updated timestamp fields
    '''
    created = models.DateTimeField("date created", auto_now_add=True)
    updated = models.DateTimeField("last updated", auto_now=True)
    deleted = models.BooleanField(_("deleted"), default=False)

    class Meta:
        abstract = True


###############
# MODELS
###############

class Project(CreateUpdateModelBase):
    """
    The Project the release notes are for.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    site = models.ForeignKey(Site, verbose_name=_("Site"), on_delete=models.CASCADE, default=settings.SITE_ID, related_name="projects")
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"))

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)      # Add check to make sure it's unique...
        super().save(*args, **kwargs)


class Release(CreateUpdateModelBase):
    """
    This is the actual release
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"))
    major = models.IntegerField(_("Major"))
    minor = models.IntegerField(_("Minor"))
    path = models.CharField(_("Patch"), max_length=50)
    published = models.BooleanField(_("Published"), default=False)

    class Meta:
        verbose_name = _("Release")
        verbose_name_plural = _("Releases")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("release_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.patch:
            self.slug = "{}.{}.{}.{}".format(slugify(self.name, allow_unicode=True), self.major, self.minor, slugify(self.patch))
        else:
            self.slug = "{}.{}.{}".format(slugify(self.name, allow_unicode=True), self.major, self.minor)
        super().save(*args, **kwargs)


class Audience(models.Model):
    """
    Users a note is targetd at.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"))
    permission = models.ForeignKey(Permission, verbose_name=_("Permission"), on_delete=models.CASCADE, related_name="permafrost_role", blank=True, null=True)

    class Meta:
        verbose_name = _("Audience")
        verbose_name_plural = _("Audiences")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Audience_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)      # Add check to make sure it's unique...
        super().save(*args, **kwargs)


class Note(CreateUpdateModelBase):
    """
    Note Sections attached to the Release.  These can be restricted to certian users via Django's permissions.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    note_type =  models.IntegerField(_("Note Type"), default=NoteType.NEW_FEATURE, choices=NoteType.choices)
    release = models.ForeignKey(Release, verbose_name=_("release"), on_delete=models.CASCADE)
    audience = models.ForeignKey(Audience, verbose_name=_("Audience"), on_delete=models.CASCADE, blank=True)
    description = models.TextField(_("Description"))
    order = models.IntegerField(_("Order"))

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Note_detail", kwargs={"pk": self.pk})
