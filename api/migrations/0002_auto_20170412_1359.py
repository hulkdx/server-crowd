# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-12 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=15)),
            ],
        ),
        migrations.DeleteModel(
            name='Greeting',
        ),
    ]
