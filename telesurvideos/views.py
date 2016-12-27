from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from .templatetags.clips_tags import get_clip, get_relacionados

class VideoView(TemplateView):
    template_name = 'clips/video.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['clip'] = get_clip(kwargs['slug'])
        if not context['clip']:
            raise Http404('Clip no existe')
        context['relacionados'] = get_relacionados(context['clip']['slug'])[:4]
        return context
        
