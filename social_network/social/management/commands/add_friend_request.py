# your_app/management/commands/create_fake_friend_requests.py

from django.core.management.base import BaseCommand
from social.models import CustomUser, FriendRequest
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Create 10 fake FriendRequest instances'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = list(CustomUser.objects.all())
        if len(users) < 2:
            self.stdout.write(self.style.ERROR('Not enough users to create friend requests.'))
            return

        for _ in range(10):
            from_user = random.choice(users)
            to_user = random.choice(users)
            
            # Ensure the from_user and to_user are not the same
            while from_user == to_user:
                to_user = random.choice(users)

            status = random.choice(['pending', 'accepted', 'rejected'])

            # Create and save the friend request
            friend_request = FriendRequest.objects.create(
                from_user=from_user,
                to_user=to_user,
                status=status
            )
            friend_request.save()

            self.stdout.write(self.style.SUCCESS(f'Friend request from {from_user.email} to {to_user.email} with status {status} created'))
