from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            return "Not found order"
        
        products = Product.objects.all()
        
        for product in products:
            order.products.add(product)
            
        order.save()
        