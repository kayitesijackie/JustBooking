# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 15:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20190429_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name=b'Date'),
        ),
    ]