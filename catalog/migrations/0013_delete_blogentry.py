# Generated by Django 4.2.4 on 2023-08-18 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_blogentry_image_alter_product_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogEntry',
        ),
    ]
