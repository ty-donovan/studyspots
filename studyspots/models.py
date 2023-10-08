from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('user', 'User')], default='user')

    def __str__(self):
        return self.username


