# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-09 09:13
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telesurvideos', '0003_auto_20170108_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videolistpluginmodel',
            name='mostrar_descripcion',
        ),
        migrations.RemoveField(
            model_name='videolistpluginmodel',
            name='mostrar_titulo',
        ),
        migrations.AddField(
            model_name='videolistpluginmodel',
            name='mostrar_descripciones',
            field=models.BooleanField(default=True, verbose_name='mostrar descripciones'),
        ),
        migrations.AddField(
            model_name='videolistpluginmodel',
            name='mostrar_titulos',
            field=models.BooleanField(default=True, verbose_name='mostrar t\xedtulos'),
        ),
        migrations.AlterField(
            model_name='videolistpluginmodel',
            name='mostrar_banner',
            field=models.BooleanField(default=False, help_text="Display first clip's banner image header", verbose_name='show banner'),
        ),
        migrations.AlterField(
            model_name='videolistpluginmodel',
            name='series',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('analysis', ''), ('revolutionary-women', ''), ('lgbt', ''), ('pachamama', ''), ('cultura-latina', '')], max_length=58, null=True, verbose_name='series'),
        ),
    ]