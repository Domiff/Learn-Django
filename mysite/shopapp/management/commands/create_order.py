from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order


class Command(BaseCommand):
     def handle(self, *args, **options):
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            addres="Tokyo",
            user=user
        )