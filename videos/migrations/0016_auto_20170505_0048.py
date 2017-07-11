# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 04:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_auto_20170505_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharecommentmodel',
            name='share',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharecomments', to='videos.ShareModel'),
        ),
        migrations.AlterField(
            model_name='sharecommentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharemodel',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='videos.VideoModel'),
        ),
    ]
