# -*- coding: utf-8 -*-
"""telesurvideos views"""
from __future__ import unicode_literals
from urllib import quote_plus

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, RedirectView

from .templatetags import clips_tags
from .models import ProgramaListPluginModel, VideoListPluginModel

class AttrDict(dict):
    """to be able to fake instances (access dict keys like attrs)"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class RedirectVideoView(RedirectView):
    """Redirect old URLs"""
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        clip = clips_tags.get_clip(kwargs['clip_slug'], lang='es') \
            or clips_tags.get_clip(kwargs['clip_slug'], lang='en')
        if not clip:
            raise Http404(_('Video no existente'))
        return clip['navegador_url']


class ProgramaView(TemplateView):
    """Programa view"""
    def get_template_names(self):
        if self.request.is_ajax():
            return ['clips/clip_list.html']
        else:
            return ['clips/programa.html']

    def get_context_data(self, **kwargs):
        context = super(ProgramaView, self).get_context_data(**kwargs)
        context['programa'] = clips_tags.get_programa(kwargs['programa_slug'])
        if not context['programa']:
            raise Http404(_('Programa no existente'))

        layout = 'eee' * 4
        mostrar_mas = 'eee' * 2
        page = int(kwargs.get('pagina', '0'))
        primero = (int(bool(page)) * len(layout) + max(page-1, 0) * len(mostrar_mas)) + 1
        page_size = len(mostrar_mas) if page else len(layout)
        context.update({
            'pagina': page,
            'instance': AttrDict(
                get_layout=mostrar_mas if page else layout,
                mostrar_mas=mostrar_mas,
                mostrar_titulos=True,
                mostrar_fecha='f',
                list_type='episode',
                page_size=page_size,
                get_items=clips_tags.get_clips({
                    'programa': context['programa']['slug'],
                    'tipo': 'programa',
                    'primero': primero,
                    'ultimo': primero + page_size - 1,
                })
            ),
        })
        return context


class VideoView(TemplateView):
    """Sinle video view"""
    #template_name = 'clips/video_videojs.html'
    template_name = 'clips/video_flowplayer.html'
    base_template = 'clips/video.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['clip'] = clips_tags.get_clip(kwargs['clip_slug'])
        if not context['clip'] or str(context['clip']['id']) != str(kwargs['clip_id']):
            raise Http404(_('Video no existente'))
        context['relacionados'] = clips_tags.get_relacionados(context['clip']['slug'])[:4]
        context.update({
            'VIDEOS_FLOWPLAYER_KEY': settings.VIDEOS_FLOWPLAYER_KEY,
            'VIDEOS_ANALYTICS': settings.VIDEOS_ANALYTICS,
        })
        return context


class ListView(TemplateView):
    """list view for AJAX pagination"""

    def dispatch(self, request, *args, **kwargs):
        self.list_type = kwargs.get('list_type')
        return super(ListView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self, **kwargs):
        return ['clips/{}_list.html'.format(self.list_type)]

    def get_plugin_instance(self, **kwargs):
        """list plugin model"""
        if kwargs['list_type'] == 'clip':
            return get_object_or_404(VideoListPluginModel, id=kwargs['list_id'])
        elif kwargs['list_type'] == 'programa':
            return get_object_or_404(ProgramaListPluginModel, id=kwargs['list_id'])

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'instance': self.get_plugin_instance(**kwargs),
            'pagina': int(kwargs['pagina']),
            })
        context.update({
            'layout': context['instance'].get_layout(context['pagina']),
            'get_items': context['instance'].get_items(context['pagina'])
            })
        context['instance'].get_items = context['get_items']
        return context


class SearchView(TemplateView):
    """search view for AJAX pagination"""
    def get_template_names(self):
        if self.request.GET.get('format') == 'atom':
            return ['clips/search_results.xml']
        elif self.request.is_ajax():
            return ['clips/search_results.html']
        else:
            return ['clips/search.html']

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('format') == 'atom':
            response_kwargs['content_type'] = 'application/rss+atom'
        return super(SearchView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'page_size': settings.VIDEOS_PAGE_SIZE,
            'page': int(self.request.GET.get('page') or 1),
            'filtros': {},
            'query': self.request.GET.get('q', '').strip(),
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
        for filtro in VideoListPluginModel.FILTROS:
            val = self.request.GET.get(filtro[0])
            if val:
                context['filtros'][filtro[0]] = val
        context['clips'] = clips_tags.get_clips(context['filtros'])

        return context
