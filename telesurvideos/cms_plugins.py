# -*- coding: utf-8 -*- #
"""telesurvideos CMS plugins"""
from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import ProgramaListPluginModel, VideoListPluginModel


class ProgramaListaPlugin(CMSPluginBase):
    """Clips lista plugin class"""
    model = ProgramaListPluginModel
    render_template = "clips/programa_list.html"
    name = _("Listado de programas teleSUR")
    module = _("teleSUR Videos")
    page_only = True
    admin_preview = True
    cache = False

plugin_pool.register_plugin(ProgramaListaPlugin)


class ClipsListaPlugin(CMSPluginBase):
    """Cliplista plugin class"""
    model = VideoListPluginModel
    render_template = "clips/clip_list.html"
    name = _("Listado de videos teleSUR")
    module = _("teleSUR Videos")
    page_only = True
    admin_preview = True
    cache = False

    fieldsets = (
        (None, {
            'fields': ('titulo',),
        }),
        (_('Opciones de despliegue'), {
            'classes': ('wide',),
            'fields': (
                'mostrar_titulos', 'mostrar_descripciones', 'mostrar_tags', 'mostrar_fecha',
                'mostrar_banner', 'layout', 'mostrar_mas',
            ),
        }),
        (_('Contenido especifífico'), {
            'classes': ('wide',),
            'fields': ('elementos',),
        }),
        (_('Filtrar por selección del editor'), {
            'classes': ('collapse',),
            'fields': ('seleccionados',),
        }),
        (_('Filtrar por tipo'), {
            'classes': ('collapse',),
            'fields': ('tipos',),
        }),
        (_('Filtrar por programa'), {
            'classes': ('collapse',),
            'fields': ('programas',),
        }),
        (_('Filtrar por categoria'), {
            'classes': ('collapse',),
            'fields': ('categorias',),
        }),
        (_('Filtrar por corresponsal'), {
            'classes': ('collapse',),
            'fields': ('corresponsales',),
        }),
        (_('Filtrar por tema'), {
            'classes': ('collapse',),
            'fields': ('temas',),
        }),
        (_('Filtrar por serie'), {
            'classes': ('collapse',),
            'fields': ('series',),
        }),
    )
plugin_pool.register_plugin(ClipsListaPlugin)
