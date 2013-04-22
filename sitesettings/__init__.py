from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from sitesettings import models

KEY = 'site-settings-%d' % settings.SITE_ID


def get_settings(from_cache=True):
    """
    Return the current site settings, firstly trying from cache, next trying to
    retrieve it from the database, finally just returning an unsaved
    SiteSettings model. If the model is retrieved from the database, it is be
    cached for future requests.

    >>> cache.set(KEY, None)

    # When no site settings exist, an unsaved SiteSettings model is returned.
    >>> s = get_settings()
    >>> print s.pk
    None

    # Retrieve the settings from the database.
    >>> s = models.SiteSettings.objects.create()
    >>> get_settings().pk == s.pk
    True

    # Further requests are retrieved it from cache.
    >>> print get_settings().archive_days
    30
    >>> s.archive_days = 90
    >>> s.save()
    >>> print get_settings().archive_days
    30
    """
    if from_cache:
        site_settings = cache.get(KEY)
        if site_settings:
            return site_settings
    try:
        site_settings = models.SiteSettings.objects.get(site__pk=settings.SITE_ID)
    except models.SiteSettings.DoesNotExist:
        site = Site.objects.get_current()
        site_settings = models.SiteSettings(site=site)
    else:
        cache.set(KEY, site_settings)
    return site_settings


def flush_settings():
    """
    Clear the current site settings from cache.

    >>> cache.set(KEY, None)

    # Save SiteSettings, then cache it.
    >>> s = models.SiteSettings.objects.create()
    >>> print get_settings().archive_days
    30

    # Now change a property.
    >>> s.archive_days = 90
    >>> s.save()

    # get_settings will still be returning the cached one.
    >>> print get_settings(None).entries_open
    30

    # Flushing will make get_settings retrieve the record from the database
    # again.
    >>> flush_settings()
    >>> print get_settings(None).entries_open
    30
    """
    cache.set(KEY, None)
