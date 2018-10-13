# -*- coding: utf-8 -*- #
"""videostelesur Models"""
from __future__ import unicode_literals, print_function
import string

from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.http.request import QueryDict
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from multiselectfield import MultiSelectField

from .templatetags import clips_tags


ASCII_LINES = {
    "L": "║", "SEP": "\n╠═══════════════════════╣\n",
    "L1": "           1           ║", "L2": "     2     ║",
    "L3": "   3   ║", "L4": "  4  ║", "L6": "        6      ║",
}

def _art(layout):
    """ASCII art layout"""
    lines = []
    for line in layout.split("\n"):
        linetxt = ASCII_LINES['L']
        for entry in line.strip(',|; '):
            if entry in ["1", "q"]:
                linetxt += ASCII_LINES['L1']
            elif entry in ["2", "w"]:
                linetxt += ASCII_LINES['L2']
            elif entry in ["3", "e"]:
                linetxt += ASCII_LINES['L3']
            elif entry in ["4", "r"]:
                linetxt += ASCII_LINES['L4']
            elif entry in ["6", "y"]:
                linetxt += ASCII_LINES['L6']
        if linetxt != ASCII_LINES['L']:
            lines.append(linetxt)
    return "╔═══════════════════════╗\n{}\n╚═══════════════════════╝".format(
        ASCII_LINES['SEP'].join(lines))

FILTROS_EXTRA = (
    {'slug': 'no_es_nulo', 'nombre': _('Tiene cualquiera')},
    {'slug': 'es_nulo', 'nombre': _('No tiene')},
)

def choices_for_filtro(filtro):
    """choices function"""
    fnc = getattr(clips_tags, 'get_%s' % filtro)
    return lazy(lambda: [(dct['slug'], dct['nombre']) for dct in FILTROS_EXTRA + tuple(fnc())], tuple)()


class BaseListPluginModel(CMSPlugin):
    """Base List Plugin Model"""
    titulo = models.CharField(_('título'), max_length=255, blank=True, help_text=_('Título opcional del listado'))
    layout = models.TextField(_('layout'), default='4444', help_text=_('1, q => columna completa | 2, w => media columna | 3, e => tercio de columna | 4, r => cuarto de columna | 6, t => dos tercios de columna'))
    mostrar_mas = models.TextField(_('mostrar más'), default='4444', blank=True, help_text=_('1, q => columna completa | 2, w => media columna | 3, e => tercio de columna | 4, r => cuarto de columna | 6, t => dos tercios de columna'))
    mostrar_titulos = models.BooleanField(_('mostrar títulos'), default=True)
    mostrar_descripciones = models.BooleanField(_('mostrar descripciones'), default=True)
    elementos = models.TextField(_('elementos'), blank=True, help_text=_('Lista con slug o ID numérico separado por comas, en caso de no especificarse ninguno, se usará el filtrado dinámico especificado.'))

    @property
    def list_type(self):
        """must implement"""
        raise NotImplementedError

    def get_layout(self, pagina=0):
        """proper layout"""
        layout = str(getattr(self, pagina and 'mostrar_mas' or 'layout'))
        return layout.translate(string.maketrans(",.|;\n\r ", '       ')).replace(' ', '')

    class Meta:
        abstract = True


class ProgramaListPluginModel(BaseListPluginModel):
    """Programa List Plugin Model"""
    MOSTRAR_PROGRAMA_CHOICES = (
        ('logo', _('Mostrar logotipo del programa')),
        ('banner', _('Mostrar banner del programa')),
        ('titulo', _('Mostrar título del programa ')),
    )
    MOSTRAR_PROGRAMA_DEFAULT = 'logo'

    mostrar_programa = models.CharField(_('mostrar programa'), choices=MOSTRAR_PROGRAMA_CHOICES, default=MOSTRAR_PROGRAMA_DEFAULT, max_length=8, null=True, blank=True)
    mostrar_horarios = models.BooleanField(_('mostrar horarios'), default=False)
    tipos = MultiSelectField(_('tipos'), choices=choices_for_filtro('tipos_programa'), null=True, blank=True, help_text=_('Filtrar únicamente los tipos de programa seleccionado'))

    @property
    def list_type(self):
        return 'programa'

    def get_items(self, pagina=0):
        """obtiene programas que representan a este objeto"""
        opts = QueryDict('', mutable=True)

        if self.tipos:
            for tipo in self.tipos:
                opts.appendlist('tipo_programa', tipo)

        primeros = len(self.get_layout(0))
        if pagina == 0:
            opts.update({'ultimo': primeros})
        else:
            segundos = len(self.get_layout(1))
            opts.update({'primero': primeros + 1 + (segundos * (pagina - 1))})
            opts.update({'ultimo': opts['primero'] + (segundos-1)})

        print(opts.urlencode())
        print('aaa')
        return clips_tags.get_programas(opts)


class VideoListPluginModel(BaseListPluginModel):
    """Video List Plugin Model"""
    FILTROS = (
        ('tipo', 'tipos'), ('programa', 'programas'),
        ('categoria', 'categorias'), ('pais', 'paises'), ('serie', 'series'),
        ('corresponsal', 'corresponsales'), ('tema', 'temas'),
    )

    MOSTRAR_FECHA_CHOICES = (
        ('rel', _('Fecha relativa (hace X tiempo)')),
        ('f', _('Fecha completa')),
        ('fh', _('Fecha completa y hora')),
        ('con', _('fecha relativa si es de hoy, fecha completa en caso contrario')),
        (None, _('No mostrar fecha')),
    )
    MOSTRAR_FECHA_DEFAULT = 'con'

    mostrar_banner = models.BooleanField(_('mostrar banner'), default=False, help_text=_('Mostrar encabezado con banner de programa correspondiente al primer video'))
    mostrar_tags = models.BooleanField(_('mostrar tags'), default=True)
    mostrar_fecha = models.CharField(_('mostrar fecha'), choices=MOSTRAR_FECHA_CHOICES, default=MOSTRAR_FECHA_DEFAULT, max_length=3, null=True, blank=True)
    limite = models.PositiveIntegerField(_('límite'), default=20)
    seleccionados = models.BooleanField(_('seleccionados'), default=False, help_text=_('Filtrar sólo clips seleccionados (selección del editor)'))
    # filtros
    tipos = MultiSelectField(_('tipos'), choices=choices_for_filtro('tipos_clip'), null=True, blank=True)
    programas = MultiSelectField(_('programas'), choices=choices_for_filtro('programas'), null=True, blank=True)
    categorias = MultiSelectField(_('categorías'), choices=choices_for_filtro('categorias'), null=True, blank=True)
    temas = MultiSelectField(_('temas'), choices=choices_for_filtro('temas'), null=True, blank=True)
    corresponsales = MultiSelectField(_('corresponsales'), choices=choices_for_filtro('corresponsales'), null=True, blank=True)
    paises = MultiSelectField(_('países'), choices=choices_for_filtro('paises'), null=True, blank=True)
    series = MultiSelectField(_('series'), choices=choices_for_filtro('series'), null=True, blank=True)

    @property
    def list_type(self):
        return 'clip'

    @property
    def cleaned_elementos(self):
        """cleaned elementos"""
        return [s.strip() for s in self.elementos.splitlines()]

    def fetch_elementos(self):
        for item in cleaned_elementos:
            digits = [int(s) for s in str.split('/') if s.isdigit()]
            if digits:
                clip = clips_tags.get_clip({'id': digits[0]})

    def get_items(self, pagina=0):
        """obtiene clips que representan a este objeto"""
        opts = QueryDict('', mutable=True)

        for filtro, attr in self.FILTROS:
            for val in getattr(self, attr):
                opts.appendlist(filtro, val)
        if self.seleccionados:
            opts.update({'seleccionado': True})

        primeros = len(self.get_layout(0))
        if pagina == 0:
            opts.update({'ultimo': primeros})
        else:
            segundos = len(self.get_layout(1))
            opts.update({'primero': primeros + 1 + (segundos * (pagina - 1))})
            opts.update({'ultimo': opts['primero'] + (segundos-1)})

        return clips_tags.get_clips(opts.urlencode())

    def __unicode__(self):
        filtros = []
        for filtro, attr in self.FILTROS:
            if getattr(self, attr):
                filtros.append('<li>{}: <strong>{}</strong></li>'.format(
                    filtro, _(' ó ').join(getattr(self, attr))))

        return mark_safe((
            '<br><pre style="display:inline-block; float:left;">''{}</pre>'
            '<ul style="max-width: 200px; margin-left: 10px; display: inline-block; float: left;">'
            '<li><h4>{}</h4></li>{}{}<li>mostrar fecha: <strong>{}</strong></li>'
            '<li>sólo seleccionados: <strong>{}</strong></li>'
            '<li>mostrar más: <strong>{}</strong></li>'
            '</ul>').format(
                _art(self.layout),
                self.titulo or '<i>[{}]</i>'.format(_('sin título')),
                ''.join(filtros),
                '<li>{}: <strong>{} / {}</strong></li>'.format(
                    _('mostrar títulos y descripciones'),
                    self.mostrar_titulos and _('sí') or _('no'),
                    self.mostrar_descripciones and _('sí') or _('no')
                ),
                self.get_mostrar_fecha_display(),
                self.seleccionados and _('sí') or _('no'),
                self.mostrar_mas and _('sí') or _('no'),
            ))
