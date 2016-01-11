from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from ringoserver.models import Device, Owner, Visitor, VisitorFaceSample, Configuration


__author__ = 'Luis Lezcano Airaldi'


class Command(BaseCommand):
    help = 'Load initial data to the database'

    def handle(self, *args, **options):
        today = timezone.now()

        # Create a group for owners
        self.stdout.write('Adding group Owners')
        owner_group = Group.objects.create(name='owners')

        # Create a group for owner's devices
        self.stdout.write('Adding group Devices')
        device_group = Group.objects.create(name='devices')

        # Create the superuser
        self.stdout.write('Creating super user')
        User.objects.create(username='ringo',
                            password=make_password('ringo-123'),
                            is_active=True,
                            is_superuser=True,
                            is_staff=True,
                            last_login=today,
                            date_joined=today)

        # Create an user for the doorbell API
        self.stdout.write('Creating doorbell user')
        doorbell_user = User.objects.create(username='doorbell',
                                            password=make_password('doorbell-123'),
                                            is_active=True,
                                            is_superuser=False,
                                            is_staff=False,
                                            last_login=today,
                                            date_joined=today)

        # Create an owner and a device
        owner_user = User.objects.create(username='luis',
                                         password=make_password('luis-123'),
                                         email='luislezcair@gmail.com',
                                         is_active=True,
                                         is_superuser=False,
                                         is_staff=False,
                                         last_login=today,
                                         date_joined=today)

        device_user = User.objects.create(username='device1',
                                          password=make_password('device1-123'),
                                          is_active=True,
                                          is_superuser=False,
                                          is_staff=False,
                                          last_login=today,
                                          date_joined=today)

        owner_user.groups.add(owner_group)
        device_user.groups.add(device_group)
    
        owner = Owner.objects.create(auth_user=owner_user)
        Device.objects.create(device_auth_user=device_user, owner=owner)

        # Add strict permissions to the doorbell user
        self.stdout.write('Adding permissions to doorbell user')

        perm_picture = Permission.objects.get(codename='add_picture')
        perm_rect = Permission.objects.get(codename='add_rect')
        doorbell_user.user_permissions.add(perm_picture, perm_rect)

        # Create some visitors
        self.stdout.write('Creating visitors')
        v1 = Visitor.objects.create(name='Luis Lezcano Airaldi')
        v2 = Visitor.objects.create(name='Andrea Lezcano Airaldi')
        v3 = Visitor.objects.create(name='Juliana Torre')

        # Create face samples for each one
        self.stdout.write('Creating visitor face samples')
        VisitorFaceSample.objects.bulk_create([
            VisitorFaceSample(picture='visitor_faces/luis/0.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/1.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/2.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/3.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/4.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/5.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/6.png', visitor=v1),
            VisitorFaceSample(picture='visitor_faces/luis/7.png', visitor=v1),

            VisitorFaceSample(picture='visitor_faces/andrea/0.png', visitor=v2),
            VisitorFaceSample(picture='visitor_faces/andrea/1.png', visitor=v2),
            VisitorFaceSample(picture='visitor_faces/andrea/2.png', visitor=v2),
            VisitorFaceSample(picture='visitor_faces/andrea/3.png', visitor=v2),
            VisitorFaceSample(picture='visitor_faces/andrea/4.png', visitor=v2),
            VisitorFaceSample(picture='visitor_faces/andrea/5.png', visitor=v2),

            VisitorFaceSample(picture='visitor_faces/juli/0.png', visitor=v3),
            VisitorFaceSample(picture='visitor_faces/juli/1.png', visitor=v3),
            VisitorFaceSample(picture='visitor_faces/juli/2.png', visitor=v3),
            VisitorFaceSample(picture='visitor_faces/juli/3.png', visitor=v3)
        ])

        self.stdout.write('Creating Configuration')
        c1 = Configuration.objects.create(id='1')
