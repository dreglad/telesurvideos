# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import VideoView, VideoListView
admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^video/(?P<slug>.*)/$', VideoView.as_view(), name="video"),
    url(r'^lista/(?P<lista_id>\d+)/(?P<pagina>\d+)/$', VideoListView.as_view(), name="video_list"),
]

#urlpatterns += i18n_patterns('',
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
