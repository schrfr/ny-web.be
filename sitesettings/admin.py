from django.contrib import admin
from sitesettings.models import SiteSettings
from forms import SiteSettingsForm


class SiteSettingsAdmin(admin.ModelAdmin):
    """
    SiteSettings Model Admin class.
    """
    fieldsets = (
        (None, {
            'fields': ('site',),
        }),
        ('Big Banner', {
            'fields': ('show_big_banner', 'big_banner', 'url_big_banner'),
        }),
        ('First Small Banner', {
            'fields': ('show_first_small_banner', 'first_small_banner', 'url_first_small_banner'),
        }),
        ('Second Small Banner', {
            'fields': ('show_second_small_banner', 'second_small_banner', 'url_second_small_banner'),
        }),
    )

admin.site.register(SiteSettings, SiteSettingsAdmin, form=SiteSettingsForm)
