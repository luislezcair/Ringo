# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ringoserver', '0003_auto_20150930_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='people',
            field=models.IntegerField(default=0),
        ),
    ]
