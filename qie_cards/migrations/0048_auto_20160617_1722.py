# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-17 22:22
from __future__ import unicode_literals

from django.db import migrations, models
import qie_cards.models


class Migration(migrations.Migration):

    dependencies = [
        ('qie_cards', '0047_auto_20160616_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='image',
            field=models.ImageField(default='default.png', upload_to=qie_cards.models.images_location),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='log_file',
            field=models.FileField(default='default.png', upload_to='uploads/lol'),
        ),
    ]
