# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0039_documentationpagemodel_rendered'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengemodel',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
