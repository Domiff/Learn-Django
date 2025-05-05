from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Product


def save_csv(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding,
    )

    reader = DictReader(csv_file)
    products = [
        Product(**row) for row in reader
    ]
    Product.objects.bulk_create(
        products,
        ignore_conflicts=True
    )
    return products
