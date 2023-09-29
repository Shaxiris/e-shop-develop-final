from django.core.cache import cache
from catalog.models import Category
from config import settings


def get_categories_cache() -> list[Category]:
    """
    Вспомогательная функция для выдачи списка категорий из кеша,
    если он там есть и если кеширование включено
    """

    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list
