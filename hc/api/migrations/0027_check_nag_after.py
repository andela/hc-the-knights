# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-18 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_after',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
