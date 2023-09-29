from django.urls import path
# from catalog.views import product, catalog, category, contacts, home, create_product
from catalog.views import ProductsListView, CategoryProductsListView, ContactsView, ProductDeleteView
from catalog.views import HomeView, ProductCreateView, ProductDetailView, ProductUpdateView
from catalog.apps import CatalogConfig
from django.views.decorators.cache import cache_page, never_cache

app_name = CatalogConfig.name

urlpatterns = [
    # path('', home, name='home'),
    path('', HomeView.as_view(), name='home'),
    # path('contacts/', contacts, name='contacts'),
    path('contacts/', cache_page(60)(ContactsView.as_view()), name='contacts'),
    # path('catalog/', catalog, name='catalog'),
    path('catalog/', cache_page(60)(ProductsListView.as_view()), name='catalog'),
    # path('<int:pk>/category/', category, name='category'),
    path('<int:pk>/category/', CategoryProductsListView.as_view(), name='category'),
    # path('creation/', create_product, name='creation'),
    path('creation_product/', never_cache(ProductCreateView.as_view()), name='creation_product'),
    # path('<int:pk>/product/', product, name='product'),
    path('<int:pk>/product/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('<int:pk>/update_product/', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('<int:pk>/delete_product/', never_cache(ProductDeleteView.as_view()), name='delete_product'),
]