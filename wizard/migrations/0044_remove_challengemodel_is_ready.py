# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 15:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0043_auto_20160902_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challengemodel',
            name='is_ready',
        ),
    ]