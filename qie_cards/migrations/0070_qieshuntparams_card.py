# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-29 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0069_auto_20160729_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='qieshuntparams',
            name='card',
            field=models.ForeignKey(default=151, on_delete=django.db.models.deletion.CASCADE, to='qie_cards.QieCard'),
        ),
    ]
