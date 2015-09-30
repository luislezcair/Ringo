# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_text', models.CharField(default=b'no message', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_text', models.CharField(max_length=200, verbose_name=b'Notification Message')),
                ('date', models.DateTimeField(verbose_name=b'Notification Date')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'photos')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('picture', models.ForeignKey(to='ringoserver.Picture')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'Date of Visit')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(default=b'Sin Apellido', max_length=200)),
                ('welcome', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitorFaceSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'visitor_faces')),
                ('visitor', models.ForeignKey(to='ringoserver.Visitor')),
            ],
        ),
        migrations.AddField(
            model_name='visit',
            name='visitor',
            field=models.ForeignKey(default=None, blank=True, to='ringoserver.Visitor', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='visitor',
            field=models.ForeignKey(to='ringoserver.Visitor'),
        ),
        migrations.AddField(
            model_name='message',
            name='visit',
            field=models.ForeignKey(to='ringoserver.Visit'),
        ),
    ]
