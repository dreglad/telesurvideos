# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-07 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telesurvideos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolistpluginmodel',
            name='mostrar_tags',
            field=models.BooleanField(default=True, verbose_name='mostrar tags'),
        ),
        migrations.AlterField(
            model_name='videolistpluginmodel',
            name='mostrar_descripcion',
            field=models.BooleanField(default=True, verbose_name='mostrar descripci\xf3n'),
        ),
        migrations.AlterField(
            model_name='videolistpluginmodel',
            name='mostrar_titulo',
            field=models.BooleanField(default=True, verbose_name='mostrar titulo'),
        ),
        migrations.AlterField(
            model_name='videolistpluginmodel',
            name='programas',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('6-grados', '6 Grados'), ('agenda-abierta', 'Agenda abierta'), ('campana-admirable', 'Campa\xf1a Admirable'), ('causa-justa', 'Causa Justa'), ('cimarrones', 'Cimarrones'), ('colores-del-futbol', 'Colores del F\xfatbol'), ('conexion-digital', 'Conexi\xf3n Digital'), ('conexion-global', 'Conexi\xf3n Global'), ('congenero', 'Cong\xe9nero'), ('cronicas-invisibles', 'Cr\xf3nicas Invisibles'), ('cruce-de-palabras', 'Cruce de Palabras'), ('de-chilena', 'De Chilena'), ('de-zurda', 'De Zurda'), ('deportes-telesur', 'Deportes teleSUR'), ('documentales', 'Documentales'), ('dossier', 'Dossier'), ('edicion-central', 'Edici\xf3n Central'), ('el-mundo-hoy', 'El Mundo Hoy'), ('el-punto-en-la-i', 'El Punto en la i'), ('en-el-medio-digital', 'En el medio digital'), ('en-juego', 'En Juego'), ('en-la-mira', 'En la mira'), ('enclave-politica', 'EnClave Pol\xedtica'), ('entre-fronteras', 'Entre Fronteras'), ('entrevista-con-jorge-gestoso', 'Entrevista con Jorge Gestoso'), ('es-noticia', 'Es Noticia'), ('expediente', 'Expediente'), ('expreso-sur', 'Expreso Sur'), ('futbol-pasion-con-eduardo-galeano', 'F\xfatbol P\xe1sion con Eduardo Galeano'), ('goles-al-bate', 'Goles al bate'), ('guia-tu-cuerpo', 'Gu\xeda tu cuerpo'), ('impacto-economico', 'Impacto Econ\xf3mico'), ('infraganti', 'Infraganti'), ('la-entrevista-decide', 'La Entrevista Decide'), ('maestra-vida', 'Maestra Vida'), ('mesa-por-la-paz', 'Mesa por la Paz'), ('mesa-redonda-internacional', 'Mesa Redonda Internacional'), ('mestizo', 'Mestizo'), ('mp3-gira-latina', 'Mp3 Gira Latina'), ('nad-especial-mundial', 'NAD Especial Mundial'), ('nad-mundo', 'NAD Mundo'), ('nad-mundo-especial-futbol', 'NAD Mundo Especial F\xfatbol'), ('no-son-tuits-son-historias', 'No son tuits, son historias'), ('nuestra-america-deportiva', 'Nuestra Am\xe9rica Deportiva'), ('pachamama', 'Pachamama'), ('palestine-travel-show', 'Palestine Travel Show'), ('paz-por-lozano', 'Paz por Lozano'), ('pedaleando-al-sur', 'Pedaleando al Sur'), ('poder', 'Poder'), ('prisma-cultural', 'Prisma Cultural'), ('programa-especial', 'Programa especial'), ('realidades', 'Realidades'), ('reportajes-telesur', 'Reportajes teleSUR'), ('reporte-360', 'Reporte 360'), ('revoluciones-en-resistencia', 'Revoluciones en Resistencia'), ('sala-a', 'Sala A'), ('siete-preguntas', 'Siete Preguntas'), ('sintesis', 'S\xedntesis'), ('tango-y-baile', 'Tango y baile'), ('telesur-noticias', 'teleSUR Noticias'), ('telesur-noticias-lenguaje-de-senas', 'TeleSUR Noticias Lenguaje de Se\xf1as'), ('temas-del-dia', 'Temas del D\xeda'), ('tras-el-telon', 'Tras el Tel\xf3n'), ('un-sabor-me-trajo-hasta-aqui', 'Un sabor me trajo hasta aqu\xed'), ('usa-de-verdad', 'USA de verdad'), ('vidas', 'Vidas'), ('voces-de-cambio', 'Voces de Cambio'), ('zona-verde', 'Zona Verde'), ('days-of-revolt', 'Days of Revolt'), ('the-empire-files', 'The Empire Files'), ('the-world-today', 'The World Today'), ('n-dont-stop', "\xd1 Don't Stop"), ('laura-flanders-show', 'Laura Flanders Show'), ('media-review', 'Media Review'), ('rear-window', 'Rear Window'), ('the-self-show', 'The Self Show'), ('interviews-from-caracas', 'Interviews from Caracas'), ('interviews-from-washington-dc', 'Interviews from Washington DC'), ('interviews-from-quito', 'Interviews from Quito'), ('interviews-from-havana', 'Interviews From Havana'), ('interviews-from-mexico', 'Interviews from Mexico'), ('atomun', 'Atomun'), ('llama-time', 'Llama Time'), ('los-nuestros', 'Los Nuestros')], max_length=1356, null=True),
        ),
    ]
