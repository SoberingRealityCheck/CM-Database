# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-18 05:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0080_rmbiasvoltage_readout_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='readoutmodule',
            name='lv_assembly',
            field=models.IntegerField(default=-1, verbose_name='LV Assembly Number'),
        ),
        migrations.AddField(
            model_name='readoutmodule',
            name='sipm_mounting',
            field=models.CharField(choices=[('1/3', '1/3'), ('2/4', '2/4')], default='', max_length=3, verbose_name='SiPM Mounting Board Type'),
        ),
        migrations.AddField(
            model_name='readoutmodule',
            name='therm_assembly',
            field=models.IntegerField(default=-1, verbose_name='Thermal Assembly Number'),
        ),
        migrations.AlterField(
            model_name='readoutmodule',
            name='odu_type',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='', max_length=3, verbose_name='ODU type'),
        ),
    ]
