# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-17 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventmodel_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventmodel',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventmodel',
            name='date',
            field=models.DateField(),
        ),
    ]
