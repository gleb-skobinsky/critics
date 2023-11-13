from django.core.management import BaseCommand
from kritika_main.models import KritikaUser
from dotenv import load_dotenv
import os

load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if KritikaUser.objects.count() == 0:
            email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
            print(f"Creating superuser account for {email}")
            admin = KritikaUser.objects.create_superuser(email=email, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')


if __name__ == "__main__":
    Command().handle()
