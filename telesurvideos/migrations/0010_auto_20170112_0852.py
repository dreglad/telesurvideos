# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-12 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telesurvideos', '0009_auto_20170112_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='programalistpluginmodel',
            name='mostrar_descripciones',
            field=models.BooleanField(default=True, verbose_name='mostrar descripciones'),
        ),
        migrations.AddField(
            model_name='programalistpluginmodel',
            name='mostrar_titulos',
            field=models.BooleanField(default=True, verbose_name='mostrar t\xedtulos'),
        ),
        migrations.AlterField(
            model_name='programalistpluginmodel',
            name='mostrar_horarios',
            field=models.BooleanField(default=False, verbose_name='mostrar horarios'),
        ),
        migrations.AlterField(
            model_name='videolistpluginmodel',
            name='mostrar_banner',
            field=models.BooleanField(default=False, help_text='Mostrar encabezado con banner de programa correspondiente al primer video', verbose_name='mostrar banner'),
        ),
    ]