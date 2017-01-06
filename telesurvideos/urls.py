# -*- coding: utf-8 -*-
"""telesurvideos URLs"""
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import SearchView, VideoView, VideoListView

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^search/$', SearchView.as_view(), name="search"),
    url(r'^lista/(?P<lista_id>\d+)/(?P<pagina>\d+)/$', VideoListView.as_view(), name="video_list"),
    url(r'^video/(?P<clip_id>\d+)/(?P<clip_slug>.+)/$', VideoView.as_view(), name="video"),
    url(r'^player/(?P<clip_id>\d+)/(?P<clip_slug>.+)/$', VideoView.as_view(), {'player': True }, name="player"),
    
]

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
