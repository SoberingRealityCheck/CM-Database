# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-29 18:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0067_qieparams_qietdcparams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qieparams',
            name='card',
        ),
        migrations.RemoveField(
            model_name='qieshuntparams',
            name='card',
        ),
        migrations.RemoveField(
            model_name='qietdcparams',
            name='card',
        ),
    ]
