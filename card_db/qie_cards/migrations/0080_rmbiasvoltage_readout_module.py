# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-10 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0079_rmbiasvoltage'),
    ]

    operations = [
        migrations.AddField(
            model_name='rmbiasvoltage',
            name='readout_module',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='qie_cards.ReadoutModule'),
        ),
    ]
