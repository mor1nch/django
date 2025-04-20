from django.core.cache import cache
from django.conf import settings

from catalog.models import Category


def get_categories():
    if settings.CACHED_ENABLED:
        key = 'categories_list'
        cache_data = cache.get(key)

        if cache_data is None:
            cache_data = list(Category.objects.all())
            cache.set(key, cache_data, 60)

        return cache_data

    return list(Category.objects.all())
