# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0045_auto_20160615_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='abbreviation',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='required',
            field=models.BooleanField(default=True),
        ),
    ]
