from django.core.mail import send_mail
from config import settings
from blog.models import BlogEntry


def send_congratulatory_email(blog_entry: BlogEntry) -> None:
    """
    Функция для оправки поздравительного сообщения пользователю
    на e-mail при достижении 100 просмотров записи блога
    """

    send_mail(
        subject='100 просмотров! Поздравляем!',
        message=f'Поздравляем!!! Ваша запись "{blog_entry.title}" достигла 100 просмотров! Вы популярны!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.RECIPIENT_EMAIL]
    )
