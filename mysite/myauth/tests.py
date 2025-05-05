from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy


class GetCookieViewTest(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:cookie-get"))
        # self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cookie value")
