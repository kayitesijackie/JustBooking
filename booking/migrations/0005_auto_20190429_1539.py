# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_schedule_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(null=True),
        ),
    ]