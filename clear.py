from django.core.management.base import BaseCommand
from accounts.models import User, Client, Counselor

class Command(BaseCommand):
    help = 'Clears data from specified models'

    def handle(self, *args, **kwargs):
        # Clear data from User model
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data cleared from User model'))

        # Clear data from Client model
        Client.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data cleared from Client model'))

        # Clear data from Counselor model
        Counselor.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data cleared from Counselor model'))
