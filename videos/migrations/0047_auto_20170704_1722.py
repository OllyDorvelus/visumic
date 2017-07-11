# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-04 21:22
from __future__ import unicode_literals

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0046_auto_20170702_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videomodel',
            name='last_edited',
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='thumbnail',
            field=models.FileField(default='vidcraftavatar.png', upload_to='thumbnails', validators=[accounts.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='title',
            field=models.CharField(max_length=115),
        ),
    ]
