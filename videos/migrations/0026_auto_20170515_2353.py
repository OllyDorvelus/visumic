# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 03:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0025_playlistmodel_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlistmodel',
            old_name='video',
            new_name='videos',
        ),
    ]
