# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-10 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0076_qieshuntparams_download'),
    ]

    operations = [
        migrations.AddField(
            model_name='qieshuntparams',
            name='failed',
            field=models.BooleanField(default=False),
        ),
    ]
