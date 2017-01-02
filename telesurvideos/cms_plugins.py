# -*- coding: utf-8 -*- #
"""telesurvideos CMS plugins"""
from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import VideoListPluginModel



class ClipsListaPlugin(CMSPluginBase):
    """Clips lista plugin class"""
    name = _("Listado de videos teleSUR")
    module = "Videos multimedia"
    model = VideoListPluginModel
    render_template = "clips/lista.html"
    page_only = True
    admin_preview = True
    cache = False

    fieldsets = (
        (None, {
            'fields': ('titulo',),
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
        (_('Opciones de despliegue'), {
            'classes': ('wide',),
            'fields': (
                'mostrar_titulo', 'mostrar_descripcion', 'tiempo', 'seleccionados',
                'mostrar_fecha', 'layout', 'mostrar_mas',
            ),
        }),
    )

plugin_pool.register_plugin(ClipsListaPlugin)
