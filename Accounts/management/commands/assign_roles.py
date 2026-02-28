from django.core.management.base import BaseCommand
from Accounts.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter(is_staff=True).update(role='LIBRARIAN')
        self.stdout.write('Roles updated.')