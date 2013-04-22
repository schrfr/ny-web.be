from django.contrib import admin
from models import *


class PersonAdmin(admin.ModelAdmin):
    """
    Person Model Admin class.
    """
    search_fields = ('first_name', 'last_name')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_display = ('__unicode__', 'user', 'email')
    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'), 'slug', 'email', 'user',)
        }),
        ("Resume", {
            'classes': ('collapse',),
            'fields': ('info',)
        }),
    )

admin.site.register(Person, PersonAdmin)

