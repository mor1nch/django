from django.db import models

from skypro_online_store import settings
from skypro_online_store.settings import NULLABLE


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, )
    description = models.TextField()
    image = models.ImageField(upload_to='images/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_per_unit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Владелец",
        **NULLABLE,
    )
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_change_description", "Can change description"),
            ("can_change_category", "Can change category"),
            ("can_change_is_published", "Can change is_published"),
        ]


class Version(models.Model):
    version_name = models.CharField(max_length=200)
    version_number = models.CharField(max_length=100, default='1.0.0')
    current_version = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, **NULLABLE, related_name='versions')

    def __str__(self):
        return f"{self.product.name} {self.version_number}"

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
