# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-10 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telesurvideos', '0005_auto_20170110_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='programalistpluginmodel',
            name='mostrar_horarios',
            field=models.BooleanField(default=True, verbose_name='mostrar banners'),
        ),
        migrations.AddField(
            model_name='programalistpluginmodel',
            name='mostrar_programa',
            field=models.CharField(blank=True, choices=[('logo', 'Mostrar logotipo del programa'), ('banner', 'Mostrar banner del programa'), ('titulo', 'Mostrar t\xedtulo del programa ')], default='con', max_length=8, null=True, verbose_name='mostrar programa'),
        ),
    ]
