# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_remove_check_is_alerted'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='is_alerted',
            field=models.BooleanField(default=False),
        ),
    ]
