# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 05:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20170422_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='comment',
            field=models.CharField(max_length=200),
        ),
    ]
