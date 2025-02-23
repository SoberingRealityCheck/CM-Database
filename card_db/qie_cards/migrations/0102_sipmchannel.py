# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-30 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0101_readoutmodule_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='SipmChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_number', models.IntegerField(default=-1)),
                ('V_30', models.CharField(max_length=50)),
                ('V_60', models.CharField(max_length=50)),
                ('V_70', models.CharField(max_length=50)),
                ('slope', models.CharField(max_length=50)),
                ('slope_error', models.CharField(max_length=50)),
                ('offset', models.CharField(max_length=50)),
                ('offset_error', models.CharField(max_length=50)),
                ('chi_squared', models.CharField(max_length=50)),
            ],
        ),
    ]
