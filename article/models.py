from django.db import models

from skypro_online_store.settings import NULLABLE


class Article(models.Model):
    title = models.CharField(max_length=255, **NULLABLE)
    slug = models.CharField(**NULLABLE)
    body = models.TextField()
    preview = models.ImageField(upload_to='article_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


