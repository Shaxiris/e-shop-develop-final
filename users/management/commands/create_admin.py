from django.core.management import BaseCommand
from users.models import User
import os


class Command(BaseCommand):
    """Класс для описания команды, создающей суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()
