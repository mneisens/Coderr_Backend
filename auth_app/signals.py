from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

@receiver(post_migrate)
def create_guest_users(sender, **kwargs):
    if sender.name == 'auth_app':
        GUEST_LOGINS = {
            'customer': {
                'username': 'andrey',
                'password': 'asdasd',
                'email': 'andrey@guest.com'
            },
            'business': {
                'username': 'kevin',
                'password': 'asdasd24',
                'email': 'kevin@guest.com'
            }
        }

        with transaction.atomic():
            for user_type, user_data in GUEST_LOGINS.items():
                username = user_data['username']
        
                if not User.objects.filter(username=username).exists():
                    # Erstelle den neuen Benutzer
                    User.objects.create_user(
                        username=username,
                        email=user_data['email'],
                        password=user_data['password'],
                        type=user_type
                    )
