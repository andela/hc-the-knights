# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-18 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20180118_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_status',
            field=models.BooleanField(default=False),
        ),
    ]
