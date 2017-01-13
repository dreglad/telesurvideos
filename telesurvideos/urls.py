# -*- coding: utf-8 -*-
"""telesurvideos URLs"""
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from .views import ListView, ProgramaView, RedirectVideoView, SearchView, VideoView

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^opensearch\.xml$',
        TemplateView.as_view(template_name='opensearch.xml', content_type='application/opensearchdescription+xml'),
        name='opensearch'),

    # Translators: search URL
    url(r'^{}$'.format(_('busqueda/')), SearchView.as_view(), name="search"),
    # Translators: list URL
    url(r'^{}(?P<list_type>clip|programa)/(?P<list_id>\d+)/(?P<pagina>\d+)/$'.format(_('lista/')), ListView.as_view(), name="list"),
    # Translators: video URL
    url(r'^{}(?P<clip_id>\d+)/(?P<clip_slug>.+)/$'.format(_('video/')), VideoView.as_view(), name="video"),
    # Translators: Shows URL
    url(r'^{}(?P<programa_slug>.+)/(?P<pagina>\d+)/$'.format(_('programas/')), ProgramaView.as_view(), name="programa"),
    url(r'^{}(?P<programa_slug>.+)/$'.format(_('programas/')), ProgramaView.as_view(), name="programa"),
    url(r'^v/(?P<clip_slug>.+)/$', RedirectVideoView.as_view(), name="redirect-video"),
    # Translators: player URL
    url(r'^{}(?P<clip_id>\d+)/(?P<clip_slug>.+)/$'.format(_('player/')), VideoView.as_view(), {'player': True }, name="player"),
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
