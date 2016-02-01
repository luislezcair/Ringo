# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doorbell_status', models.BooleanField(default=True)),
                ('out_of_house_mode', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_auth_user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'photos')),
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
                ('date', models.DateTimeField(auto_now_add=True)),
                ('people', models.IntegerField(default=0)),
                ('picture', models.ForeignKey(blank=True, to='ringoserver.Picture', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('welcome', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitorFaceSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'visitor_faces')),
                ('visitor', models.ForeignKey(related_name='face_samples', to='ringoserver.Visitor')),
            ],
        ),
        migrations.AddField(
            model_name='visit',
            name='visitors',
            field=models.ManyToManyField(to='ringoserver.Visitor', blank=True),
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
        migrations.AddField(
            model_name='device',
            name='owner',
            field=models.ForeignKey(to='ringoserver.Owner'),
        ),
    ]
