from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product


class OrderListTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob", password="hello")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(username="bob", password="hello")

    def test_order_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("shopapp:orders"))
        self.assertContains(response, "Orders")


class ProductCreateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Test Product", price=100)
        cls.user = User.objects.create_superuser(username="bob", password="hello")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def setUp(self):
        self.client.login(username="bob", password="hello")

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_get_product(self):
        response = self.client.get(reverse("shopapp:products"))
        self.assertContains(response, self.product.name)
