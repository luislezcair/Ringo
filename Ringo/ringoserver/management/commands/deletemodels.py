from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from ringoserver.models import Device, Owner, Visitor, VisitorFaceSample


__author__ = 'Luis Lezcano Airaldi'


class Command(BaseCommand):
    help = 'Removes all created entities from the database'

    def handle(self, *args, **options):
        self.stdout.write('Deleting users...')
        User.objects.all().delete()

        self.stdout.write('Deleting groups...')
        Group.objects.all().delete()

        self.stdout.write('Deleting owners...')
        Owner.objects.all().delete()

        self.stdout.write('Deleting devices...')
        Device.objects.all().delete()

        self.stdout.write('Deleting visitor face samples...')
        VisitorFaceSample.objects.all().delete()

        self.stdout.write('Deleting visitors...')
        Visitor.objects.all().delete()