# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-26 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_check_member_allowed_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='member_allowed_email',
        ),
        migrations.AddField(
            model_name='check',
            name='member_allowed_id',
            field=models.IntegerField(default=0),
        ),
    ]
