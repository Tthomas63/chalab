# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-22 13:43
from __future__ import unicode_literals

import bundler.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundler', '0005_auto_20160922_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundletaskmodel',
            name='output',
            field=models.FileField(null=True, upload_to=bundler.models.StorageNameFactory('data', 'bundles')),
        ),
    ]