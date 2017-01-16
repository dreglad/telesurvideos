# -*- coding: utf-8 -*- #
"""
telesurvideos Spanish site settings
"""
from __future__ import unicode_literals
from settings import *

SITE_ID = 1

LANGUAGE_CODE = 'es'

LANGUAGES = (
    ('es', gettext('es')),
)

CACHES['default']['KEY_PREFIX'] = 'es'

CELERY_BROKER_URL = 'redis://localhost:6379/0'

VIDEOS_EXCLUDE_CATEGORIAS = (
    'con-nombre-de-mujer', 'zona-verde', 'al-pulso-de-venezuela',
    'al-pulso-de-ecuador', 'a-nivel-del-sur',
)

VIDEOS_EXCLUDE_TIPOS = ('tematico',)
VIDEOS_EXCLUDE_TEMAS = ()
VIDEOS_EXCLUDE_CATEGORIAS = ()
VIDEOS_EXCLUDE_CORRESPONSALES = ()
VIDEOS_EXCLUDE_PAISES = ()
VIDEOS_EXCLUDE_SERIES = ()

try:
    from local_settings import *
except ImportError:
    pass

try:
    from local_settings_es import *
except ImportError:
    pass
