# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-13 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_event_note_field_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='note',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
    ]