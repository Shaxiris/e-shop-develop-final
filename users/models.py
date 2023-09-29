from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель для описания пользователя, в качестве основного идентификатора используется e-mail"""

    username = None

    email = models.EmailField(unique=True, verbose_name='E-mail')

    avatar = models.ImageField(blank=True,
                               null=True,
                               upload_to='users/',
                               default='users/anonim.jpg',
                               verbose_name='Аватар')

    phone = models.CharField(blank=True, null=True, max_length=60, verbose_name='Телефон')
    country = models.CharField(blank=True, null=True, max_length=60, verbose_name='Страна')

    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    verification_code = models.CharField(max_length=10,
                                         unique=True,
                                         null=True,
                                         blank=True,
                                         verbose_name='Код верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

