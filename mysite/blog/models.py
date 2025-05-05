from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(null=True, blank=True, max_length=500)
    published_at = models.DateTimeField()

    def get_absolute_url(self):
        return reverse("blog:article", kwargs={"pk": self.pk})
