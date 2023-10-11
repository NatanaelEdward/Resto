from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import UserProfile
from menuapp.models import DataMeja

class Command(BaseCommand):
    help = 'Create users and associate them with DataMeja instances'

    def handle(self, *args, **options):
        # Create or retrieve a user (replace 'username' and 'password' with actual values)
        user = User.objects.create_user(username='meja2', password='meja2')

        # Create a DataMeja instance for the user (choose a table for the user)
        data_meja = DataMeja.objects.get(nomor_meja='2')  # Replace 'Table1' with the desired table number

        # Create or update the user's UserProfile to associate it with the DataMeja
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.data_meja = data_meja  # Associate the user with the DataMeja
        user_profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully created users with DataMeja associations'))
