# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0038_remove_playlistmodel_playlistimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='videos.GenreModel'),
        ),
    ]
