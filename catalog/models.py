from django.db import models

from users.models import User


# Create your models here.
class Category(models.Model):
    """
    Модель для описания категории товара
    """

    name = models.CharField(
                        max_length=100,
                        verbose_name='Наименование'
                    )
    description = models.TextField(
                        verbose_name='Описание'
                    )
    image = models.ImageField(
                        upload_to='categories/',
                        null=True,
                        blank=True,
                        verbose_name='Изображение'
                    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )


class Product(models.Model):
    """
    Модель для описания товара
    """

    name = models.CharField(
                            max_length=100,
                            verbose_name='Наименование'
                        )
    description = models.TextField(
                            verbose_name='Описание'
                        )
    image = models.ImageField(
                            default='products/default.png',
                            upload_to='products/',
                            null=True,
                            blank=True,
                            verbose_name='Изображение'
                        )
    category = models.ForeignKey(
                            Category,
                            on_delete=models.CASCADE,
                            verbose_name='Категория'
                        )
    price = models.DecimalField(
                            max_digits=8,
                            decimal_places=2,
                            verbose_name='Стоимость'
                        )
    owner = models.ForeignKey(
                            User,
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name='Владелец'
                        )
    creation_date = models.DateTimeField(
                            auto_now_add=True,
                            verbose_name='Дата создания'
                        )
    change_date = models.DateTimeField(
                            auto_now=True,
                            verbose_name='Дата последнего изменения'
                        )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('change_date', 'name', )


class Contact(models.Model):
    """
    Модель для описания контактных данных
    """

    name = models.CharField(max_length=100, verbose_name='Страна')
    inn = models.CharField(max_length=30, verbose_name='ИНН')
    address = models.CharField(max_length=500, verbose_name='Адрес')

    def __str__(self):
        return f"{self.name}, {self.inn}, {self.address}"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Version(models.Model):

    """Модель для описания версии товара"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    number = models.PositiveSmallIntegerField(verbose_name='Номер версии')
    name = models.CharField(max_length=100, verbose_name='Название версии')
    status = models.BooleanField(default=True, verbose_name='Активная версия')

    def __str__(self):
        return f"{self.name}: {self.number}, {self.status}"

    def save(self, *args, **kwargs):
        if self.status:
            Version.objects.filter(product=self.product, status=True).update(status=False)
        super(Version, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'