# -*- coding: utf-8 -*- #
from __future__ import unicode_literals, print_function
import string
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from multiselectfield import MultiSelectField
from cms.models.pluginmodel import CMSPlugin
from django.http.request import QueryDict, MultiValueDict
from django.db import models
from django.utils.encoding import smart_text

from .templatetags import clips_tags

def _art(layout):
    """ascii art layout"""
    L = "║"
    SEP = "\n╠═══════════════════════╣\n"
    L1  = "           1           ║"
    L2  = "     2     ║"
    L3  = "   3   ║"
    L4  = "  4  ║"
    L6  = "        6      ║"
    lines = []
    for line in layout.split("\n"):
        linetxt = L
        for entry in line.strip(',|; '):
            if   entry in ["1", "q"]: linetxt += L1
            elif entry in ["2", "w"]: linetxt += L2
            elif entry in ["3", "e"]: linetxt += L3
            elif entry in ["4", "r"]: linetxt += L4
            elif entry in ["6", "y"]: linetxt += L6
        if linetxt != L:
            lines.append(linetxt)
    return "╔═══════════════════════╗\n{}\n╚═══════════════════════╝".format(
        SEP.join(lines))

def tipos_choices():
    """tipos"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_tipos()]

def corresponsales_choices():
    """corresponsales"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_corresponsales()]

def programas_choices():
    """programas"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_programas()]

def series_choices():
    """programas"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_series()]

def paises_choices():
    """programas"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_paises()]

def temas_choices():
    """temas"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_temas()]

def categorias_choices():
    """temas"""
    return [(c['slug'], c['nombre']) for c in clips_tags.get_categorias()]

MOSTRAR_FECHA_CHOICES = (
    ('rel', 'Fecha relativa (hace X tiempo)'),
    ('f', 'Fecha completa'),
    ('fh', 'Fecha completa y hora'),
    ('con', 'fecha relativa si es de hoy, fecha completa en caso contrario'),
    (None, 'No mostrar fecha'),
)
MOSTRAR_FECHA_DEFAULT = 'con'

def tiempo_choices():
    """tiempo choices"""
    return (
        (None, '- Sin restricción -'),
        ('1h', '1 hora'), ('3h', '3 horas'), ('12h', '12 horas'), ('1d', '1 día'),
        ('2d', '2 días'), ('3d', '3 días'), ('1s', '1 semana'), ('2s', '2 semanas'),
        ('1e', '1 mes'), ('2e', '2 meses'), ('1a', '1 año'), ('2', '2 años'),
    )

class VideoListPluginModel(CMSPlugin):
    """VideoLista"""
    layout = models.TextField(blank=True, help_text='1, q => columna completa | 2, w => media columna | 3, e => tercio de columna | 4, r => cuarto de columna | 6, t => dos tercios de columna')
    mostrar_mas = models.TextField('mostrar más', blank=True, help_text='1, q => columna completa | 2, w => media columna | 3, e => tercio de columna | 4, r => cuarto de columna | 6, t => dos tercios de columna')
    mostrar_titulo = models.BooleanField('mostrar_titulo', default=True)
    titulo = models.CharField('título', max_length=255, blank=True, help_text='Título opcional del listado')
    mostrar_descripcion = models.BooleanField('mostrar_descripción', default=True)
    limite = models.PositiveIntegerField('límite', default=20)
    tiempo = models.CharField(choices=tiempo_choices(), max_length=8, null=True, blank=True, help_text='Mostrar videos no más antiguos del tiempo especificado')
    seleccionados = models.BooleanField(default=False, help_text='Filtrar sólo clips seleccionados (selección del editor)')
    # filtros
    tipos = MultiSelectField(choices=lazy(tipos_choices, tuple)(), null=True, blank=True)
    programas = MultiSelectField(choices=lazy(programas_choices, tuple)(), null=True, blank=True)
    categorias = MultiSelectField('categorías', choices=lazy(categorias_choices, tuple)(), null=True, blank=True)
    temas = MultiSelectField(choices=lazy(temas_choices, tuple)(), null=True, blank=True)
    corresponsales = MultiSelectField(choices=lazy(corresponsales_choices, tuple)(), null=True, blank=True)
    paises = MultiSelectField('países', choices=lazy(paises_choices, tuple)(), null=True, blank=True)
    series = MultiSelectField('series', choices=lazy(series_choices, tuple)(), null=True, blank=True)
    mostrar_fecha = models.CharField(choices=MOSTRAR_FECHA_CHOICES, default=MOSTRAR_FECHA_DEFAULT, max_length=3, null=True, blank=True)

    FILTROS = (
        ('tipo', 'tipos'), ('programa', 'programas'),
        ('categoria', 'categorias'), ('pais', 'paises'),
        ('serie', 'series'), ('corresponsal', 'corresponsales'),
        ('tema', 'temas'),
    )

    def _cleaned(self, value):
        """cleaned value"""
        return str(value).translate(string.maketrans(",.|;\n\r ", '       ')).replace(' ', '')

    def get_layout(self, pagina=0):
        """proper layout"""
        attr = pagina and 'mostrar_mas' or 'layout'
        return self._cleaned(getattr(self, attr))

    @property
    def cleaned_mostrar_mas(self):
        return self._cleaned(self.mostrar_mas)

    @property
    def cleaned_layout(self):
        """cleaned layout"""
        return self._cleaned(self.layout)

    def get_clips(self, pagina=0):
        """obtiene clips que representan a este objeto"""
        opts = QueryDict('', mutable=True)

        for filtro, attr in self.FILTROS:
            for val in getattr(self, attr):
                opts.appendlist(filtro, val)
        if self.tiempo:
            opts.update({'tiempo': self.tiempo})
        if self.seleccionados:
            opts.update({'seleccionado': True})

        primeros = len(self.cleaned_layout)
        if pagina == 0:
            opts.update({'ultimo': primeros})
        else:
            segundos = len(self.cleaned_mostrar_mas)

            opts.update(
                {'primero': primeros + 1 + (segundos * (pagina - 1))})
            opts.update(
                {'ultimo': opts['primero'] + (segundos-1)})

        import pprint
        pprint.pprint(opts)
        return clips_tags.get_clips(opts.urlencode())

    def __unicode__(self):
        filtros = []
        for filtro, attr in self.FILTROS:
            if getattr(self, attr):
                filtros.append('<li>{}: <strong>{}</strong></li>'.format(
                    filtro, ' ó '.join(getattr(self, attr))))

        if self.tiempo:
            filtros.append('<li>tiempo: <strong>{}</strong></li>'.format(self.get_tiempo_display()))

        return mark_safe((
            '<br><pre style="display:inline-block; float:left;">''{}</pre>'
            '<ul style="max-width: 200px; margin-left: 10px; display: inline-block; float: left;">'
            '<li><h4>{}</h4></li>{}{}<li>mostrar fecha: <strong>{}</strong></li>'
            '<li>sólo seleccionados: <strong>{}</strong></li>'
            '<li>mostrar más: <strong>{}</strong></li>'
            '</ul>').format(
                _art(self.layout),
                self.titulo or '<i>[sin título]</i>',
                ''.join(filtros),
                '<li>mostrar título y descripción: <strong>{} / {}</strong></li>'.format(
                    self.mostrar_titulo and 'sí' or 'no',
                    self.mostrar_descripcion and 'sí' or 'no'
                ),
                self.get_mostrar_fecha_display(),
                self.seleccionados and 'sí' or 'no',
                self.mostrar_mas and 'sí' or 'no',
            ))
