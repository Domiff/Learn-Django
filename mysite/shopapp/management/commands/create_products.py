from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """
    Create new products
    """
    
    def handle(self, *args, **options):
        
        products_names = [
            "Laptop",
            "Desktop",
            "Phone",
        ]
        
        for products_name in products_names:
            product, created = Product.objects.get_or_create(name=products_name)
            self.stdout.write(f"Was created {product}")