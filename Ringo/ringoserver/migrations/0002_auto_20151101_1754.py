# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ringoserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorfacesample',
            name='visitor',
            field=models.ForeignKey(related_name='face_samples', to='ringoserver.Visitor'),
        ),
    ]
