# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='country',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='height',
        ),
        migrations.RemoveField(
            model_name='users',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='weight',
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
