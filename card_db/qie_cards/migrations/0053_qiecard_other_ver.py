# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0052_auto_20160624_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='qiecard',
            name='other_ver',
            field=models.CharField(default='', max_length=8),
        ),
    ]
