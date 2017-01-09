# -*- coding: utf-8 -*-
"""template tags"""
from __future__ import unicode_literals
import datetime
import re
import urllib
import requests

from cacheback.decorators import cacheback
from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime 
from django.template import defaultfilters, Node, TemplateSyntaxError, VariableDoesNotExist
from django.utils.translation import ugettext as _


register = template.Library()

if settings.SITE_ID == 1: # es
    BASE_API = 'http://multimedia.telesurtv.net/api/'
elif settings.SITE_ID == 2: #en
    BASE_API = 'http://multimedia.telesurtv.net/en/api/'

def clip_parser(dct):
    """convert from JSON"""
    if 'fecha' in dct:
        try:
            dct['fecha'] = datetime.datetime.strptime(dct['fecha'], "%Y-%m-%d %H:%M:%S")
        except:
            pass

        if 'idioma' in dct:
            if dct['idioma'] != 'en' or (dct.get('programa') and (dct['programa']['idioma'] == 'es' or dct['programa'].get('slug') in ['just-cause'])):
                dct['width'] = 640
                dct['height'] = 480
            else:
                dct['width'] = 1280
                dct['height'] = 720
            dct['aspectratio'] = dct['height'] / float(dct['width'])
    return dct

@cacheback(lifetime=60, fetch_on_miss=True)
def get_api(url):
    """gets API parsed JSON response"""
    try:
        request = requests.get(BASE_API + url)
        if request.status_code == 200:
            return request.json(object_hook=datetime_parser)
        else:
            return []
    except:
        print "ERROR"
        return []


# custom templatetags and filters

@register.filter
def index(a_list, i):
    """gets the i-th element from a_list sequence"""
    try:
        return a_list[int(i)]
    except IndexError:
        pass


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_clip(slug, params=''):
    """get single clip"""
    return get_api('clip/{}/?detalle=completo&{}'.format(
        urllib.quote(slug), params
        ))


@register.assignment_tag
@cacheback(lifetime=60*20, fetch_on_miss=True)
def get_relacionados(slug, params=''):
    """get related clips"""
    return get_api('clip/?relacionados={}&detalle=completo&tiempo=3e&{}'.format(
        urllib.quote(slug), params
        ))


@register.assignment_tag
@cacheback(lifetime=60*2, fetch_on_miss=True)
def get_clips(params=''):
    """return clips"""
    return get_api('clip/?detalle=completo&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_series(params=''):
    """return series"""
    return get_api('serie/?ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_temas(params=''):
    """temas list"""
    return get_api('tema/?ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_categorias(params=''):
    """categorias list"""
    return get_api('categoria/?ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_programas(params=''):
    """programas list"""
    return get_api('programa/?detalle=completo&ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*24, fetch_on_miss=True)
def get_programa(slug):
    """single programa"""
    return get_api('programa/{}/'.format(slug))


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_paises(params=''):
    """países list"""
    return get_api('pais/?&ultimo=300&{}'.format(params))


@register.assignment_tag
def get_tipos(params=''):
    """tipos list"""
    return get_api('tipo_clip/?ultimo=300&{}'.format(params))


@register.assignment_tag
def get_corresponsales(params=''):
    """corresponsales list"""
    return get_api('corresponsal/?ultimo=300&{}'.format(params))


@register.assignment_tag
def get_list_clips(videolist, pagina=0):
    """paginated clips"""
    return videolist.get_clips(pagina)


@register.assignment_tag
def get_list_layout(videolist, pagina=0):
    """list layout corresponding to page"""
    return videolist.get_layout(pagina)

@register.filter
def print_fecha(fecha, lista):
    """humanized date for clip in list"""
    today = datetime.date.today()
    if (lista.mostrar_fecha == 'rel'
            or (lista.mostrar_fecha == 'con' and fecha.date() == today)):
        return naturaltime(fecha)

    if lista.mostrar_fecha in ['f', 'con']:
        if today.year == fecha.year:
            # Translators: Full date format within current year
            return defaultfilters.date(fecha, _(r"j \d\e F"))
        else:
            # Translators: Full date format not in current year
            return defaultfilters.date(fecha, _(r"j \d\e F \d\e Y"))

    if lista.mostrar_fecha == 'fh':
        if today.year == fecha.year:
            # Translators: Full date & time format within current year
            return defaultfilters.date(fecha, _(r"j \d\e F, H:i \h\r\s."))
        else:
            # Translators: Full date & time format not within current year
            return defaultfilters.date(fecha, _(r"j \d\e F \d\e Y, H:i \h\r\s."))

@register.filter
def print_duration(date):
    """format duration"""
    if date.startswith('00:'):
        return date[3:]
    return date

@register.simple_tag(takes_context=True)
def title_for_search(context):
    filtros = context['filtros']
    title = ''
    if filtros.get('tipo'):
        tipo = filter(lambda x: x['slug'] == filtros['tipo'], get_tipos())
        if tipo:
            title += tipo[0]['nombre_plural'] + ' '
            if filtros['tipo'] == 'programa' and filtros.get('programa'):
                programa = get_programa(filtros['programa'])
                if programa:
                    return '"{}", programas completos grabadas'.format(programa['nombre'])
    if filtros.get('corresponsal'):
        corresponsal = get_corresponsal(filtros['corresponsal'])
        if corresponsal:
            title = (title or 'Videos ') + 'de {} '.format(corresponsal['nombre'])
            if corresponsal['twitter']:
                title += '(@{}) '.format(corresponsal['twitter']) 

    if context.get('query'):
        title = 'Búsqueda '
    return ((title or "Búsqueda ") + ' | Videoteca').strip()



