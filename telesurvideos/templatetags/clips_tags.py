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
from django.http.request import QueryDict
from django.template import defaultfilters, Node, TemplateSyntaxError, VariableDoesNotExist
from django.utils.translation import ugettext as _


register = template.Library()

BASE_API = {
    'es': 'http://multimedia.telesurtv.net/api/',
    'en': 'http://multimedia.telesurtv.net/en/api/',
    'pt': 'http://multimedia.telesurtv.net/pt/api/',
}

def clip_parser(dct):
    """convert from JSON"""
    if 'fecha' in dct:
        try:
            dct['fecha'] = datetime.datetime.strptime(dct['fecha'], "%Y-%m-%d %H:%M:%S")
        except:
            pass

        if 'idioma' in dct:
            if dct['idioma'] != 'en' or (dct.get('programa') and (dct['programa']['idioma'] == 'es' or dct['programa'].get('slug') in ['know-your-body', 'just-cause'])):
                dct['width'] = 640
                dct['height'] = 480
            else:
                dct['width'] = 1280
                dct['height'] = 720
            dct['aspectratio'] = dct['height'] / float(dct['width'])
    return dct

@cacheback(lifetime=60, fetch_on_miss=True)
def get_api(path, lang=None):
    """gets API parsed JSON response"""
    try:
        url = BASE_API[lang or settings.LANGUAGE_CODE]
        request = requests.get(url + path)
        print 'request to ', url + path
        if request.status_code == 200:
            return request.json(object_hook=clip_parser)
        else:
            return []
    except Exception, e:
        print "ERROR: {}".format(e.message)
        return []


@register.filter
def index(sequence, i):
    """gets the i-th element from sequence"""
    try:
        return sequence[int(i)]
    except IndexError:
        pass


@register.assignment_tag
@cacheback(lifetime=60*60*2, fetch_on_miss=True)
def get_clip(slug, params='', lang=None):
    """get single clip"""
    return get_api('clip/{}/?detalle=completo&{}'.format(
        urllib.quote(slug), params, lang=None
        ))


@register.assignment_tag
@cacheback(lifetime=60*10, fetch_on_miss=True)
def get_relacionados(slug, params=''):
    """get related clips"""
    return get_api('clip/?relacionados={}&detalle=completo&tiempo=3e&{}'.format(
        urllib.quote(slug), params
        ))


@register.assignment_tag
@cacheback(lifetime=60*2, fetch_on_miss=True)
def get_clips(params=''):
    """return clips"""
    if isinstance(params, QueryDict):
        params = params.urlencode()
    elif isinstance(params, dict):
        qdict = QueryDict('', mutable=True)
        qdict.update(params)
        params = qdict.urlencode()
    print params
    return get_api('clip/?detalle=completo&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*24, fetch_on_miss=True)
def get_series(params=''):
    """return series"""
    return get_api('serie/?ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60, fetch_on_miss=True)
def get_temas(params=''):
    """temas list"""
    return get_api('tema/?ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*24, fetch_on_miss=True)
def get_categorias(params=''):
    """categorias list"""
    return get_api('categoria/?ultimo=300&{}'.format(params))


@register.assignment_tag
@cacheback(lifetime=60*60*12, fetch_on_miss=True)
def get_programas(params=''):
    """programas list"""
    if isinstance(params, QueryDict):
        params = params.urlencode()
    elif isinstance(params, dict):
        qdict = QueryDict('', mutable=True)
        qdict.update(params)
        params = qdict.urlencode()
    return get_api('programa/?detalle=completo&ultimo=300&idioma={}&{}'.format(
        settings.LANGUAGE_CODE, params))


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


@cacheback(lifetime=60*60*12, fetch_on_miss=True)
@register.assignment_tag
def get_tipos_programa(params=''):
    """tipos list"""
    return get_api('tipo_programa/?ultimo=300&{}'.format(params))


@cacheback(lifetime=60*60*12, fetch_on_miss=True)
@register.assignment_tag
def get_tipos_clip(params=''):
    """tipos list"""
    return get_api('tipo_clip/?ultimo=300&{}'.format(params))


@cacheback(lifetime=60*60*12, fetch_on_miss=True)
@register.assignment_tag
def get_corresponsales(params=''):
    """corresponsales list"""
    return get_api('corresponsal/?ultimo=300&{}'.format(params))

@register.assignment_tag
@cacheback(lifetime=60*60*12, fetch_on_miss=True)
def get_corresponsal(slug):
    """single programa"""
    return get_api('corresponsal/{}/'.format(slug))


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
        tipo = filter(lambda x: x['slug'] == filtros['tipo'], get_tipos_clip())
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



