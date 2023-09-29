from django import template
from django.db import models
from config import settings

register = template.Library()


@register.simple_tag
def mediapath(object: models.Model) -> str:
    """Шаблонный тег для построения пути к медиафайлам приложения"""

    if object and object.image and hasattr(object.image, 'url'):
        return object.image.url
    return f'{settings.MEDIA_URL}blog/default.jpg'


@register.filter
def mediapath(object: models.Model) -> str:
    """Шаблонный фильтр для построения пути к медиафайлам приложения"""

    if object and object.image and hasattr(object.image, 'url'):
        return object.image.url
    return f'{settings.MEDIA_URL}blog/default.jpg'