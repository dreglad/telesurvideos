# -*- coding: utf-8 -*-
"""telesurvideos views"""
from __future__ import unicode_literals
from urllib import quote_plus

from django.conf import settings
from django.http import Http404
from django.http.request import QueryDict
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from .templatetags.clips_tags import get_clip, get_clips, get_relacionados
from .models import FILTROS, VideoListPluginModel


class VideoView(TemplateView):
    """Sinle video view"""
    template_name = 'clips/video_flowplayer.html'

    base_template = 'clips/video.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['clip'] = get_clip(kwargs['clip_slug'])
        if not context['clip'] or str(context['clip']['id']) != str(kwargs['clip_id']):
            raise Http404(_('Video no existente'))
        context['relacionados'] = get_relacionados(context['clip']['slug'])[:4]
        context.update({
            'VIDEOS_FLOWPLAYER_KEY': settings.VIDEOS_FLOWPLAYER_KEY,
            'VIDEOS_ANALYTICS': settings.VIDEOS_ANALYTICS,
        })
        return context


class VideoListView(TemplateView):
    """video list view for AJAX pagination"""
    template_name = 'clips/lista.html'

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        context['instance'] = get_object_or_404(VideoListPluginModel, id=kwargs['lista_id'])
        context['pagina'] = int(kwargs['pagina'])
        return context


class SearchView(TemplateView):
    """search view for AJAX pagination"""
    def get_template_names(self):
        if self.request.is_ajax():
            return ['clips/search_results.html']
        else:
            return ['clips/search.html']

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'page_size': settings.VIDEOS_PAGE_SIZE,
            'page': int(self.request.GET.get('page', 1)),
            'filtros': QueryDict('', mutable=True),
            'query': self.request.GET.get('q', ''),
            'exclude': {
                'tipos': settings.VIDEOS_EXCLUDE_TIPOS,
                'categorias': settings.VIDEOS_EXCLUDE_CATEGORIAS,
                'temas': settings.VIDEOS_EXCLUDE_TEMAS,
                'corresponsales': settings.VIDEOS_EXCLUDE_CORRESPONSALES,
                'paises': settings.VIDEOS_EXCLUDE_PAISES,
                'series': settings.VIDEOS_EXCLUDE_SERIES,
            },
        })
        context['filtros'].update({
            'primero': 1 + (settings.VIDEOS_PAGE_SIZE*(context['page']-1)),
            'ultimo': settings.VIDEOS_PAGE_SIZE*context['page'],
        })
        if context['query']:
            context['filtros']['texto'] = context['query']
        for filtro in FILTROS:
            val = self.request.GET.get(filtro[0])
            if val:
                context['filtros'][filtro[0]] = val
        context['clips'] = get_clips(context['filtros'].urlencode())

        return context
