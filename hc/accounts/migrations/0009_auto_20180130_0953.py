# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-30 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_member_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['priority']},
        ),
    ]
