# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from .models import VideoListPluginModel


class ClipsListaPlugin(CMSPluginBase):
    name = _("Listado de videos teleSUR")
    module = "Videos multimedia"
    model = VideoListPluginModel
    page_only = True
    admin_preview = True
    render_template = "clips/lista.html"
    cache = False

    fieldsets = (
        (None, {
            'fields': ('titulo',),
        }),
        ('Filtrar por tipo', {
            'classes': ('collapse',),
            'fields': ('tipos',),
        }),
        ('Filtrar por programa', {
            'classes': ('collapse',),
            'fields': ('programas',),
        }),
        ('Filtrar por categoria', {
            'classes': ('collapse',),
            'fields': ('categorias',),
        }),
        ('Filtrar por corresponsal', {
            'classes': ('collapse',),
            'fields': ('corresponsales',),
        }),
        ('Filtrar por tema', {
            'classes': ('collapse',),
            'fields': ('temas',),
        }),
        ('Filtrar por serie', {
            'classes': ('collapse',),
            'fields': ('series',),
        }),
        ('Opciones generales', {
            'classes': ('wide',),
            'fields': ('mostrar_titulo', 'mostrar_descripcion', 'tiempo', 'layout'),
        }),

    )

    def render(self, context, instance, placeholder):
        context = super(ClipsListaPlugin, self).render(context, instance, placeholder)

        return context

plugin_pool.register_plugin(ClipsListaPlugin)