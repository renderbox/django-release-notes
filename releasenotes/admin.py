from django.contrib import admin

from .models import Project, Release, Audience, Note, Translation

###############
# MODEL INLINE
###############

# class TranslationInline(admin.TabularInline):
#     model = Translation
#     extra = 1

###############
# MODEL ADMINS
###############

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'deleted',
        'site',
    )
    list_filter = ('created', 'updated', 'deleted', 'site')
    search_fields = ('name',)
    readonly_fields = ['slug']


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'deleted',
        'major',
        'minor',
        'patch',
        # 'published',
    )
    list_filter = ('created', 'updated', 'deleted', 'project') #, 'published')
    search_fields = ('name',)
    readonly_fields = ['slug']


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'permission')
    list_filter = ('project', 'permission')
    search_fields = ('name',)
    readonly_fields = ['slug']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'deleted',
        'release',
        'note_type',
        'description',
        'order',
    )
    list_filter = ('created', 'updated', 'deleted', 'release')
    # inlines = [TranslationInline]


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    pass
    # list_display = (
    #     'name',
    #     'deleted',
    #     'site',
    # )
    # list_filter = ('created', 'updated', 'deleted', 'site')
    # search_fields = ('name',)
    # readonly_fields = ['slug']
