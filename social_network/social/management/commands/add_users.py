# your_app/management/commands/create_fake_users.py

from django.core.management.base import BaseCommand
from social.models import CustomUser
from faker import Faker


class Command(BaseCommand):
    help = 'Create 10 fake CustomUser instances'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):
            email = fake.unique.email()
            username = fake.user_name()
            password = fake.password()  

            # Create and save the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()

            self.stdout.write(self.style.SUCCESS(f'User {email} created'))
