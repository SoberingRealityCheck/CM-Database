# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-27 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0112_calibrationunit_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibrationunit',
            name='cu_uid',
            field=models.CharField(blank=True, default='', max_length=6),
        ),
    ]
