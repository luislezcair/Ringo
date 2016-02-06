# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ringoserver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'owner_profiles'),
        ),
    ]
