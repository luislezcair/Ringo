# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ringoserver', '0002_auto_20150930_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='surname',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='visitor',
        ),
        migrations.AddField(
            model_name='visit',
            name='visitors',
            field=models.ManyToManyField(to='ringoserver.Visitor'),
        ),
    ]
