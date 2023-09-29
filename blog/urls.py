from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from blog.views import BlogEntryListView, BlogEntryCreateView, BlogEntryUnpublishedListView
from blog.views import BlogEntryDetailView, publish_blog_entry, BlogEntryUpdateView, BlogEntryDeleteView
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', cache_page(60)(BlogEntryListView.as_view()), name='blog'),
    path('unpublished_entries/', BlogEntryUnpublishedListView.as_view(), name='unpublished_entries'),
    path('new_entry/', never_cache(BlogEntryCreateView.as_view()), name='new_entry'),
    path('entry/<slug:slug>/', cache_page(60)(BlogEntryDetailView.as_view()), name='blog_entry'),
    path('activity/<slug:slug>/', never_cache(publish_blog_entry), name='publish'),
    path('update_entry/<slug:slug>/', never_cache(BlogEntryUpdateView.as_view()), name='update_entry'),
    path('delete_entry/<slug:slug>/', never_cache(BlogEntryDeleteView.as_view()), name='delete_entry'),
]