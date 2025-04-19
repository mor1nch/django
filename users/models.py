from django.contrib.auth.models import AbstractUser
from django.db import models

from skypro_online_store.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=30, unique=True, verbose_name="Номер телефона", **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name="аватар", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="страна", **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"