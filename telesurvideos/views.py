# -*- coding: utf-8 -*-
"""telesurvideos views"""
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .templatetags.clips_tags import get_clip, get_relacionados
from .models import VideoListPluginModel

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
