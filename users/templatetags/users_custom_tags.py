from django import template
from config import settings
from users.models import User

register = template.Library()


@register.simple_tag
def mediapath(object: User) -> str:
    """Шаблонный тег для построения пути к медиафайлам приложения"""

    if object and object.avatar and hasattr(object.avatar, 'url'):
        return object.avatar.url
    return f'{settings.MEDIA_URL}users/anonim.jpg'


@register.filter
def mediapath(object: User) -> str:
    """Шаблонный фильтр для построения пути к медиафайлам приложения"""

    if object and object.avatar and hasattr(object.avatar, 'url'):
        return object.avatar.url
    return f'{settings.MEDIA_URL}users/anonim.jpg'
