import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import Permission
from django.utils.text import slugify

###
# HELPERS - TO NOT TRIGGER MIGRATIONS ON USER'S SITES
###

def get_default_site(*args, **kwargs):
    return settings.SITE_ID

def get_default_language_code(*args, **kwargs):
    return settings.LANGUAGE_CODE

def get_languages(*args, **kwargs):
    return settings.LANGUAGES

###############
# CHOICES
###############



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
    site = models.ForeignKey(Site, verbose_name=_("Site"), on_delete=models.CASCADE, default=get_default_site, related_name="projects")
    slug = models.SlugField(_("Slug"))

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("releasenotes:project-details", kwargs={"project_slug": self.slug})

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)      # Add check to make sure it's unique on the site
        super().save(*args, **kwargs)


class Release(CreateUpdateModelBase):
    """
    This is the actual release
    """

    class ReleaseState(models.IntegerChoices):
        FUTURE = 0, _("Future Release")
        CURRENT = 10, _("Current Release")
        PREVIOUS = 20, _("Previous Release")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=True)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE, related_name="releases")
    slug = models.SlugField(_("Slug"), blank=True)
    major = models.IntegerField(_("Major"))
    minor = models.IntegerField(_("Minor"))
    patch = models.CharField(_("Patch"), max_length=50, blank=True)
    state =  models.IntegerField(_("Release State"), default=ReleaseState.CURRENT, choices=ReleaseState.choices)

    class Meta:
        verbose_name = _("Release")
        verbose_name_plural = _("Releases")

    @property
    def version_number(self):
        result = [str(self.major), str(self.minor)]
        if self.patch:
            result.append(slugify(self.patch))

        return ".".join(result)

    @property
    def version_name(self):
        if not self.name:
            return "v{}".format(self.version_number)
        return "v{} - {}".format(self.version_number, self.name)

    def __str__(self):
        return self.project.name + " - " + self.version_name

    def get_absolute_url(self):
        return reverse("releasenotes:release-details", kwargs={"release_slug": self.slug, "project_slug": self.project.slug})

    def save(self, *args, **kwargs):
        self.slug = ".".join([slugify(part, allow_unicode=True) for part in self.version_name.split(".")])      # This is done to keep the periods in the slug
        # TODO: If this is changed to current, make sure there are no other are set to current
        super().save(*args, **kwargs)


class Audience(models.Model):
    """
    Users a note is targetd at.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=80, blank=False)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE, related_name="audiences")
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

    class NoteType(models.IntegerChoices):
        NEW_FEATURE = 0, _("New Features")
        BUG_FIX = 10, _("Bug Fixes")
        KNOWN_ISSUES = 20, _("Known Issues")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    note_type =  models.IntegerField(_("Note Type"), default=NoteType.NEW_FEATURE, choices=NoteType.choices)
    release = models.ForeignKey(Release, verbose_name=_("release"), on_delete=models.CASCADE, related_name="notes")
    audience = models.ForeignKey(Audience, verbose_name=_("Audience"), on_delete=models.CASCADE, blank=True, null=True, related_name="release_notes")
    description = models.TextField(_("Description"))
    order = models.IntegerField(_("Order"), blank=True, default=0, help_text="The lower the number, the closer to the top of the list the note apears")

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        unique_together = ['release', 'note_type', 'audience']

    def __str__(self):
        if self.audience:
            return str(self.release) + " " + self.audience + " Note"
        return str(self.release) + " Note"

    def get_absolute_url(self):
        return reverse("releasenotes:note-detail", kwargs={"pk": self.pk})


class Translation(CreateUpdateModelBase):
    '''
    This provides a mechanism to have localized release notes
    '''
    class LANGUAGES(models.TextChoices):        # TODO: Move to use django language lists
        EN_US = "en-us", _("English - US")
        JA = "ja", _("Japanese")

    note = models.ForeignKey(Note, verbose_name=_("Note"), on_delete=models.CASCADE, related_name="translations")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    language = models.CharField(_("Language"), max_length=7, blank=False, default=get_default_language_code )   # Can't use Choices because it will trigger a migration.  Need to put choices in forms and use a custom validator.
    description = models.TextField(_("Description"))

    def __str__(self):
        return str(self.note) + " - " + self.language
