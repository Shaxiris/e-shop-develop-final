from django.core.management import BaseCommand
from catalog.models import Product, Category
from django.apps import apps
from pathlib import Path
from django.db import connection, transaction, models
import json


class Command(BaseCommand):
    """
    Класс для описания команды для автоматического очищения базы данных от старых данных и
    заполнения новыми, полученными из файлов, находящихся в директории catalog_filling
    """

    # пути к конкретным файлам, содержащим данные для заполнения БД
    products_path = Path('./catalog/catalog_filling/products.json')
    categories_path = Path('./catalog/catalog_filling/categories.json')

    @staticmethod
    def read_datafile(data_path: Path) -> list[dict] | None:
        """Вспомогательный метод, предназначенный для чтения файлов с данными для записи"""

        if data_path.exists() and data_path.is_file():
            try:
                with open(data_path, 'r', encoding='UTF-8') as json_file:
                    return json.load(json_file)
            except Exception:
                return

    @staticmethod
    def clear_db(models: tuple[models.Model]) -> None:
        """Вспомогательный метод, предназначенный для очищения таблиц в базе данных"""

        with transaction.atomic():
            for model in models:
                model.objects.all().delete()

    @staticmethod
    def reset_sequence(models: tuple[models.Model]) -> None:
        """Вспомогательный метод, предназначенный для сброса счетчика автоинкремента в базе данных"""

        for model in models:
            table_name = model._meta.db_table
            sequence_name = f"{table_name}_id_seq"
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")
                connection.commit()

    def handle(self, *args, **options) -> None:
        """Основное действие команды.

        1) Очищает базу данных
        2) Сбрасывает счетчик автоинкремента
        3) заполняет базу данных новыми данными из файлов
        """

        app_name = self.__module__.split('.')[0]
        app_config = apps.get_app_config(app_name)
        models = tuple(app_config.get_models())

        # очищаем старые значения БД и сбрасываем счетчик
        self.clear_db(models)
        self.reset_sequence(models)

        categories = self.read_datafile(self.categories_path)
        products = self.read_datafile(self.products_path)

        for category_info in categories:
            name = category_info.get('name')
            category = Category(**category_info)
            category.save()
            products_info = []
            for product in products:
                if product.get('category') == name:
                    product['category'] = category
                    products_info.append(Product(**product))
            Product.objects.bulk_create(products_info)
