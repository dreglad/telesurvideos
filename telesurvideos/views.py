# -*- coding: utf-8 -*-
"""telesurvideos views"""
from urllib import quote_plus
from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .templatetags.clips_tags import get_clip, get_clips, get_relacionados
from .models import FILTROS, VideoListPluginModel


class VideoView(TemplateView):
    """Sinle video view"""
    template_name = 'clips/video_flowplayer.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['clip'] = get_clip(kwargs['slug'])
        if not context['clip']:
            raise Http404('Clip no existe')
        context['relacionados'] = get_relacionados(context['clip']['slug'])[:4]
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
        context['page_size'] = settings.VIDEOS_PAGE_SIZE
        context['page'] = int(self.request.GET.get('page', 1))
        context['query'] = self.request.GET.get('q', '')
        context['exclude_categorias'] = settings.VIDEOS_EXCLUDE_CATEGORIAS or []
        context['exclude_tipos'] = settings.VIDEOS_EXCLUDE_TIPOS or []

        context['filtros'] = {}
        params = ''
        for filtro, nombre in FILTROS:
            val = self.request.GET.get(filtro)
            if val:
                params += '{}={}&'.format(filtro, quote_plus(val))
                context['filtros'][filtro] = val

        if self.request.GET.get('tiempo'):
            context['tiempo'] = self.request.GET.get('tiempo')
            params += 'tiempo={}&'.format(context['tiempo'])
        if context['query']:
            params += 'texto={}&'.format(quote_plus(context['query']))

        params += 'primero={}&ultimo={}'.format(
            1 + (context['page_size']*(context['page']-1)),
            context['page_size']*context['page'],
            )
        context['clips'] = get_clips(params)

        return context