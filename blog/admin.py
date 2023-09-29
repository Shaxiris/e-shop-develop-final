from django.contrib import admin
from blog.models import BlogEntry


# Register your models here.


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    """
    Отображение записи блога
    """
    list_display = ('pk', 'title', 'slug', 'content', 'image', 'creation_date', 'is_published', 'number_views')
    search_fields = ('title', 'content')
    list_filter = ('is_published',)