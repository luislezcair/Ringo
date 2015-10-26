# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.utils import timezone


def create_users(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    Owner = apps.get_model('ringoserver', 'Owner')
    Device = apps.get_model('ringoserver', 'Device')

    db_alias = schema_editor.connection.alias

    # Create a group for owners
    owner_group = Group.objects.using(db_alias).create(name='owners')

    # Create a group for owner's devices
    device_group = Group.objects.using(db_alias).create(name='devices')

    # Create the superuser
    User.objects.using(db_alias).create(username='ringo',
                                        password=make_password('ringo-123'),
                                        email='ringo@ringosystems.com.ar',
                                        is_active=True,
                                        is_superuser=True,
                                        is_staff=True,
                                        last_login=timezone.now(),
                                        date_joined=timezone.now())

    # Create an owner and a device
    owner_user = User.objects.using(db_alias).create(username='luis',
                                                     password=make_password('luis-123'),
                                                     email='luislezcair@gmail.com',
                                                     is_active=True,
                                                     is_superuser=False,
                                                     is_staff=False,
                                                     last_login=timezone.now(),
                                                     date_joined=timezone.now())

    device_user = User.objects.using(db_alias).create(username='device1',
                                                      password=make_password('device1-123'),
                                                      is_active=True,
                                                      is_superuser=False,
                                                      is_staff=False,
                                                      last_login=timezone.now(),
                                                      date_joined=timezone.now())

    owner_user.groups.add(owner_group)
    device_user.groups.add(device_group)

    owner = Owner.objects.using(db_alias).create(auth_user=owner_user)
    Device.objects.using(db_alias).create(device_auth_user=device_user, owner=owner)


def delete_users(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    Owner = apps.get_model('ringoserver', 'Owner')
    Device = apps.get_model('ringoserver', 'Device')

    db_alias = schema_editor.connection.alias

    User.objects.using(db_alias).all().delete()
    Group.objects.using(db_alias).all().delete()

    Owner.objects.using(db_alias).all().delete()
    Device.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ringoserver', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users, reverse_code=delete_users)
    ]
