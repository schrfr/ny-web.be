from django.contrib import admin
from models import *


class LinkAdmin(admin.ModelAdmin):
    """
    Link Model Admin class.
    """
    list_display = ('title', 'url', 'category')
    search_fields = ('title', 'url', 'category')
    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'category')
        }),
        ("Resume", {
            'classes': ('collapse',),
            'fields': ('description',)
        }),
    )

admin.site.register(Link, LinkAdmin)


class LinkCategoryAdmin(admin.ModelAdmin):
    """
    LinkCategory Admin class
    """
    list_display = ('name', 'order')
    list_editable = ('order',)
    prepopulated_fields = {"identifier": ("name",)}
    fieldsets = (
        (None, {
            'fields': ('name', 'identifier')
        }),
    )

admin.site.register(LinkCategory, LinkCategoryAdmin)