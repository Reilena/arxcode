# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-17 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exploration', '0033_auto_20181117_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='weight_spawn',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
