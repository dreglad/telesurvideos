# -*- coding: utf-8 -*- #
"""telesuvideos context processors"""
from django.conf import settings

def newrelic(request):
    """pass Newrelic App ID if present in settings"""
    if hasattr(settings, 'NEWRELIC_APPLICATION_ID'):
        return {'NEWRELIC_APPLICATION_ID': settings.NEWRELIC_APPLICATION_ID}