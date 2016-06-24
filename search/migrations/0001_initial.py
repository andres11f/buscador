# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import search.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contenidoAyer', models.FileField(upload_to=search.models.Contenido.url)),
                ('contenidoHoy', models.FileField(upload_to=search.models.Contenido.url)),
            ],
        ),
        migrations.CreateModel(
            name='Enlace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('enlace', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Patron',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=20)),
                ('semilla', models.URLField()),
                ('pais', models.CharField(max_length=20)),
                ('ciudad', models.CharField(max_length=20)),
                ('patron', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Patrones',
            },
        ),
        migrations.AddField(
            model_name='enlace',
            name='patron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Patron'),
        ),
        migrations.AddField(
            model_name='contenido',
            name='enlace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Enlace'),
        ),
        migrations.AddField(
            model_name='contenido',
            name='patron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Patron'),
        ),
    ]