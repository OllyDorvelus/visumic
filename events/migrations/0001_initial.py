# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-16 21:08
from __future__ import unicode_literals

import accounts.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('street_address', models.CharField(max_length=100)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('city', models.CharField(max_length=50)),
                ('picture', models.FileField(upload_to='event_pictures', validators=[accounts.validators.validate_file_extension])),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attending', models.ManyToManyField(blank=True, related_name='attend', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='created_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]