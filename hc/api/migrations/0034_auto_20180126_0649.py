# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-26 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20180125_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='member_allowed_access',
            field=models.BooleanField(default=False),
        ),
    ]
