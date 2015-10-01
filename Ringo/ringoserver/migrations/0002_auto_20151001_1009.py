# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ringoserver', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='surname',
        ),
        migrations.AddField(
            model_name='visit',
            name='picture',
            field=models.ForeignKey(default=None, blank=True, to='ringoserver.Picture', null=True),
        ),
    ]
