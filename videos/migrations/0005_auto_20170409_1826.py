# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 22:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20170409_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
