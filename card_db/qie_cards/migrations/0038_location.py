# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0037_auto_20160614_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_recieved', models.DateTimeField(verbose_name='date recieved')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qie_cards.QieCard')),
            ],
        ),
    ]
