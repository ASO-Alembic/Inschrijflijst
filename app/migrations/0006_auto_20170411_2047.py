# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-11 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170403_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='published_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='setting',
            name='value',
            field=models.TextField(blank=True),
        ),
    ]
