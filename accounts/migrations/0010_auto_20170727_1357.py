# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-27 17:57
from __future__ import unicode_literals

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170531_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_banner',
            field=models.FileField(default='vbanner.jpg', upload_to='profile_banners', validators=[accounts.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_img',
            field=models.FileField(default='vidcraftavatar.png', upload_to='profile_pics', validators=[accounts.validators.validate_file_extension]),
        ),
    ]