from django.contrib.auth.models import User
from django.db import models


def product_preview_path(instance, filename):
    return "products/products_{pk}/preview/{filename}".format(
        pk=instance.pk, filename=filename
    )


class Product(models.Model):
    """
    Модель Product представляет товар для онлайн магазина

    Заказы тут:  :model:`shopapp.Order`
    """
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=50)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_path)

    def __str__(self):
        return self.name


def product_image_path(instance, filename):
    return "products/products_{pk}/preview/{filename}".format(
        pk=instance.product.pk, filename=filename
    )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(null=True, blank=True, upload_to=product_image_path)


class Order(models.Model):
    addres = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, blank=True, upload_to="orders/receipts/")


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()
