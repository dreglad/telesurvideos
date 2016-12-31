# -*- coding: utf-8 -*-
"""template tags"""
import requests
import re
import datetime
import urllib

from django import template
from cacheback.decorators import cacheback

BASE_API = 'http://multimedia.telesurtv.net/api/'

register = template.Library()


def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, basestring) and re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", v):
            try:
                dct[k] = datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except:
                pass
    return dct


@register.filter
def index(a_list, i):
    try:
        return a_list[int(i)]
    except:
        return None

def get_api(url):
    """Get api json"""
    r = requests.get(BASE_API + url)
    print url
    if r.status_code == 200:
        return r.json(object_hook=datetime_parser)
    else:
        return []


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_clip(slug, params=''):
    """return clips"""
    return get_api('clip/' + urllib.quote(slug) + '/?detalle=completo&' + params)


@register.assignment_tag
@cacheback(lifetime=60*20, fetch_on_miss=True)
def get_relacionados(slug, params=''):
    """return clips"""
    return get_api('clip/?relacionados=' + urllib.quote(slug) + '&detalle=completo&tiempo=3e' + params)


@register.assignment_tag
@cacheback(lifetime=60*2, fetch_on_miss=True)
def get_clips(params=''):
    """return clips"""
    return get_api('clip/?detalle=completo&' + params)


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_series(params=''):
    """return series"""
    return get_api('serie/?ultimo=300&' + params)


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_temas(params=''):
    """return temas"""
    return get_api('tema/?ultimo=300&' + params)


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_categorias(params=''):
    """return categorias"""
    return get_api('categoria/?ultimo=300&' + params)


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_programas(params=''):
    """return programas"""
    return get_api('programa/?detalle=normal&ultimo=300&' + params)


@register.assignment_tag
@cacheback(lifetime=60*60*48, fetch_on_miss=True)
def get_paises(params=''):
    """return programas"""
    return get_api('pais/?&ultimo=300&' + params)



@register.assignment_tag
def get_tipos(params=''):
    """return tipos"""
    return get_api('tipo_clip/?ultimo=300&' + params)


@register.assignment_tag
def get_corresponsales(params=''):
    """return corresponsales"""
    return get_api('corresponsal/?ultimo=300&' + params)

@register.filter
def es_hoy(date):
    """hoy"""
    return datetime.date.today() == date

@register.filter
def es_anoactual(date):
    """hoy"""
    return datetime.date.today().year == date.year
