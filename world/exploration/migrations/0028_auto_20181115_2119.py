# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-15 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exploration', '0027_shardhavenobstacleroll_damage_splash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shardhavenlayout',
            name='haven',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='layout', to='exploration.Shardhaven'),
        ),
    ]
