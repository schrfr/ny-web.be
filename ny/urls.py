from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from library.feeds import LatestEntries
from hardcopies.models import PrintIssue

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^share/(?P<slug>[-\w]+)/$', 'share.views.share', name="ny-share"),
)

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)

urlpatterns += patterns('django.contrib.syndication.views',
    url(r'^feeds/latest/$', LatestEntries(), name="ny-feed-latest"),
)

urlpatterns += patterns('ny.views',
    url(r'^dereactor/$', 'dereactor', {}, name="ny-dereactor"),
    url(r'^about/(?P<iso_code>\w{2})/$', 'about', {}, name="ny-about"),
)

    
urlpatterns += patterns('django.views.generic.simple',
    url(r'^workshop/$', 'direct_to_template', {'template': 'workshop.html'}, name='ny-workshop'),
)

urlpatterns += patterns('links.views',
    url(r'^links/$', 'links', {}, name="ny-links"),
)

urlpatterns += patterns('hardcopies.views',
    url(r'^print-issues/$', 'archive_redirect', {}),
    url(r'^print-issues/(?P<slug>[-\w]+)/$', 'archive_redirect', {}, name="ny-hard-copy"),
    url(r'^print-issues/(?P<magazine_slug>[-\w]+)/(?P<issue_slug>[-\w]+)/$', 'hard_copy', {}, name="ny-hard-copy-detail"),
)

urlpatterns += patterns('library.views',
    url(r'^$', 'timeline', {}, name="ny-timeline"),
    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+).html$', 'text', {}, name="ny-text"),
)

urlpatterns += patterns('library.views',
    url(r'^search/$', 'search', {}, name="ny-search"),
    url(r'^web-archive/$', 'list_new', { 'archive': True }, name="ny-archive-all"),
    url(r'^web-archive/(?P<field>\w+)/(?P<query>[-\w]+)/$', 'list_new', { 'archive': True }, name="ny-archive-filtered"),
    url(r'^(?P<category>[-\w]+)/$', 'list_new', { 'archive': False }, name="ny-list"),
    url(r'^(?P<category>[-\w]+)/(?P<field>\w+)/(?P<query>[-\w]+)/$', 'list_new', { 'archive': False }, name="ny-list-filtered"),
)



#if settings.LOCAL_DEV:
    #baseurlregex = r'^static/(?P<path>.*)$'
    #urlpatterns += patterns('',
        #(baseurlregex, 'django.views.static.serve', {'document_root':  settings.MEDIA_ROOT}),
    #)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
