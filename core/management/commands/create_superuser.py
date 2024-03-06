from core.models import BaseUser
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Create a superuser if one does not exist"

    def handle(self, *args, **options):
        username = "admin"
        password = "vesatogo"
        email = "admin@vesatogo.com"

        if settings.GQ_ENV not in ["production"]:
            if not BaseUser.objects.filter(username=username).exists():
                BaseUser.objects.create_superuser(username, email, password)
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created successfully.')
                )
            else:
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists.'))
