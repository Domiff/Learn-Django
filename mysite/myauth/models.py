from django.contrib.auth.models import User
from django.db import models

from shopapp.user_model import MyUser


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
