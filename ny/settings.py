# -*- coding: utf-8 -*-
# Django settings for ny project.

import os.path
import os

LOCAL_DEV = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Alexandre Leray', 'alexandre@stdin.fr'),
)

MANAGERS = ADMINS

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'NAME': os.path.join(PROJECT_DIR, 'ny.db'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

gettext = lambda s: s
LANGUAGES = (
    ('fr', gettext('French')),
    ('en', gettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticis')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xb(*r#)@^wd&1e6m^d7#%g9mgyta(2$s-qrk@p5@qxk^f%y8p('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "sitesettings.context_processors.banners"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'ny.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.flatpages',
    'django.contrib.markup',
    'threadedcomments',
    'django.contrib.comments',
    'django.contrib.humanize',
    'django_extensions',
    'tinymce',
    'sorl.thumbnail',
    'filebrowser',
    'library',
    'people',
    'hardcopies',
    'custom_tags',
    'links',
    'sitesettings',
    'chunks',
)

# DATE_FORMAT = 'F Y, the jS'

#FILEBROWSER_IMAGE_GENERATOR_LANDSCAPE = [('thumbnail_',97),('small_',97),('medium_',359),('big_',620)]
#FILEBROWSER_IMAGE_GENERATOR_PORTRAIT = [('thumbnail_',97),('small_',97),('medium_',359),('big_',620)]
# Versions Format. Available Attributes: verbose_name, width, height, opts
FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': 'Thumbnail (97px)', 'width': 97, 'height': '', 'opts': ''},
    'small': {'verbose_name': 'Small (97px)', 'width': 97, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (359px)', 'width': 359, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (620px)', 'width': 620, 'height': '', 'opts': ''},
    'cropped': {'verbose_name': 'Cropped (60x60px)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'croppedthumbnail': {'verbose_name': 'Cropped Thumbnail (140x140px)', 'width': 140, 'height': 140, 'opts': 'crop'},
}

# Override the server-derived value of SCRIPT_NAME 
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

# TINYMCE_JS_URL (default: settings.MEDIA_URL + 'js/tiny_mce/tiny_mce.js')
#     The URL of the TinyMCE javascript file.
# TINYMCE_JS_ROOT (default: settings.MEDIA_ROOT + 'js/tiny_mce')
#     The filesystem location of the TinyMCE files.
# TINYMCE_DEFAULT_CONFIG (default: {'theme': "simple", 'relative_urls': False})
#     The default TinyMCE configuration to use. See the TinyMCE manual for all options. To set the configuration for a specific TinyMCE editor, see the mce_attrs parameter for the widget.
# TINYMCE_SPELLCHECKER (default: False)
#     Whether to use the spell checker through the supplied view. You must add spellchecker to the TinyMCE plugin list yourself, it is not added automatically.
# TINYMCE_COMPRESSOR (default: False)
#     Whether to use the TinyMCE compressor, which gzips all Javascript files into a single stream. This makes the overall download size 75% smaller and also reduces the number of requests. The overall initialization time for TinyMCE will be reduced dramatically if you use this option.
# TINYMCE_FILEBROWSER (default: True if 'filebrowser' is in INSTALLED_APPS, else False)
#     Whether to use django-filebrowser as a custom filebrowser for media inclusion. See the official TinyMCE documentation on custom filebrowsers.
# 
# Example:
# 
# TINYMCE_JS_URL = 'http://debug.example.org/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "fullscreen,paste,searchreplace,emotions",
    'theme': "advanced",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_fonts' : "Arial=arial,helvetica,sans-serif;Courier New=courier new,courier,monospace;Georgia=Georgia,'Times New Roman',Times,serif",
    'theme_advanced_buttons1_add' : ", fontselect, forecolor",
    'theme_advanced_buttons3_add' : ",|,blockquote, |,emotions,|,search,replace,|,pastetext,pasteword,selectall,|,fullscreen",
    'theme_advanced_blockformats' : "p,h1,h2,h3,h4,blockquote",
}

## — find and replace
# — quotation
## — paste
## — paste from word
## — paste as plain text
## — find
## — emoticons
## — toggle full-screen mocde

TINYMCE_SPELLCHECKER = True
# TINYMCE_COMPRESSOR = True

COMMENTS_APP = 'threadedcomments'

COMMENTS_ALLOW_PROFANITIES = True
