# Generated by Django 4.2.4 on 2023-08-15 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/media/default.png', null=True, upload_to='products/', verbose_name='Изображение'),
        ),
    ]
