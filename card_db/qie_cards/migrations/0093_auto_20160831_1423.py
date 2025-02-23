# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-31 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0092_auto_20160829_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembler', models.CharField(default='', max_length=50, verbose_name='Assembler')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of Assembly')),
                ('place', models.CharField(default='', max_length=50, verbose_name='Location of Assembly')),
                ('cu_number', models.IntegerField(default=-1, verbose_name='Calibration Unit \u2116')),
                ('pulser_board', models.IntegerField(default=-1, verbose_name='Pulser Board \u2116')),
                ('optics_box', models.IntegerField(default=-1, verbose_name='Optics Box \u2116')),
                ('pindiode_led1', models.IntegerField(default=-1, verbose_name='Pindiode_LED1 \u2116')),
                ('pindiode_led2', models.IntegerField(default=-1, verbose_name='Pindiode_LED2 \u2116.')),
                ('pindiode_laser1', models.IntegerField(default=-1, verbose_name='Pindiode board_laser1 \u2116')),
                ('pindiode_laser2', models.IntegerField(default=-1, verbose_name='Pindiode board_laser2 \u2116')),
                ('pindiode_laser3', models.IntegerField(default=-1, verbose_name='Pindiode board_laser3 \u2116')),
                ('pindiode_laser4', models.IntegerField(default=-1, verbose_name='Pindiode board_laser4 \u2116')),
                ('upload', models.FileField(default='default.png', upload_to='cu_calibration/', verbose_name='QC Data File')),
                ('qc_complete', models.BooleanField(default=False, verbose_name='QC Complete')),
                ('qie_card', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qie_cards.QieCard', verbose_name='QIE Card \u2116')),
            ],
        ),
        migrations.RemoveField(
            model_name='cu',
            name='qie_card',
        ),
        migrations.DeleteModel(
            name='CU',
        ),
    ]
