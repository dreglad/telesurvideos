# -*- coding: utf-8 -*- #
"""
Django settings for telesurvideos project.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os

gettext = lambda s: s
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'f%o_$vfpki#3!&)9-t39w8(lyuq(6q1#e!qif5@ca2s=^(g#7d'

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = []

SITE_ID = 1

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',

    'analytical',
    'compressor',
    'corsheaders',
    'django_celery_results',
    'cacheback',

    'multiselectfield',
    'django.contrib.humanize',

    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_link',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_utils',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_picture',
    'telesurvideos'
)

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': 'localhost',
        'NAME': os.path.join(DATA_DIR, 'project.db'),
        'PASSWORD': '',
        'PORT': '',
        'USER': ''
    }
}

ROOT_URLCONF = 'telesurvideos.urls'
WSGI_APPLICATION = 'telesurvideos.wsgi.application'

# Languages

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('es', gettext('es')),
)

CMS_LANGUAGES = {
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'es',
            'hide_untranslated': False,
            'name': gettext('es'),
            'redirect_on_fallback': True,
        },
    ],
}


# Static files

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'telesurvideos', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'telesurvideos', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.debug',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.csrf',
                'django.core.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.core.context_processors.static',
                'cms.context_processors.cms_settings'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'cacheback': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# telesurvideos


VIDEOS_ANALYTICS = ''
VIDEOS_FLOWPLAYER_KEY = ''

VIDEOS_PAGE_SIZE = 10

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

# Django CMS

CMS_TEMPLATES = (
    ('simple.html', gettext('Simple')),
    ('sin_header_footer.html', gettext('Sin header ni footer')),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {
    None: {
        "plugins": ['ClipsListaPlugin', 'TextPlugin', 'PicturePlugin', 'LinkPlugin'],
        'text_only_plugins': ['LinkPlugin', 'PicturePlugin'],
    }
}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

try:
    from local_settings import *
except ImportError:
    pass
