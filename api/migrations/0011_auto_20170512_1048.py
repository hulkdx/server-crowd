# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-12 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20170510_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=b'', max_length=80),
        ),
        migrations.AddField(
            model_name='category',
            name='source_fill',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]