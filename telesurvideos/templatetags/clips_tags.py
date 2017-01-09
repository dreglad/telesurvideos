# -*- coding: utf-8 -*-
"""template tags"""
import requests
import re
import datetime
import urllib
import time

from django import template
from cacheback.decorators import cacheback


BASE_API = 'http://multimedia.telesurtv.net/api/'

register = template.Library()

def datetime_parser(dct):
    """convert JSON dates into datetime"""
    for k, v in dct.items():
        dct['width'] = 640
        dct['height'] = 480
        if isinstance(v, basestring) and re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", v):
            try:
                dct[k] = datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except:
                pass
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
def print_duration(date):
    """format duration"""
    if date.startswith('00:'):
        return date[3:]
    return date

@register.filter
def es_hoy(date):
    """is today"""
    return datetime.date.today() == date


@register.filter
def es_anoactual(date):
    """is current year"""
    return datetime.date.today().year == date.year
