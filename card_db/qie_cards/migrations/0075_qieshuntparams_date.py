# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-10 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0074_auto_20160729_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='qieshuntparams',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]
