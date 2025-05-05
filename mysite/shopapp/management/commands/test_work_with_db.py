from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Avg, Min, Max, Count, Sum

from shopapp.models import Order, Product


class Command(BaseCommand):
     def handle(self, *args, **options):
        products_list = Product.objects.aggregate(
            Avg("price"),
            Min("price"),
            Max("price"),
            Count("id"),
        )

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0)
        )

        for order in orders:
            print(order.total)

        # print(products_list)
