from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet, Prefetch
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from catalog import services
from config.settings import ENTRY_PATH
from catalog.models import Product, Contact, Category, Version
from catalog.forms import ProductForm, VersionForm

# Create your views here.
COUNT_LATEST_PRODUCTS = 5


# def home(request: WSGIRequest) -> HttpResponse:
#     """
#     Контроллер для отображения домашней страницы
#     """
#     context = {
#         'product_list': Product.objects.order_by('-change_date')[:5],
#         'category_list': Category.objects.all()
#     }
#     return render(request, 'catalog/home.html', context)


class HomeView(TemplateView):
    """
    Класс-контроллер для отображения домашней страницы
    """

    template_name = 'catalog/home.html'
    extra_context = {
        'product_list': Product.objects.order_by('-change_date')[:COUNT_LATEST_PRODUCTS],
        'category_list': services.get_categories_cache()
    }


# def contacts(request: WSGIRequest) -> HttpResponse:
#     """
#     Контроллер для отображения страницы с контактами и обратной связью
#     """
#     context = {
#         'contact_data': Contact.objects.get(pk=2),
#     }
#     if request.method == "POST":
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         with open(ENTRY_PATH, "a", encoding="UTF-8") as file:
#             print(f'You have new message from {name}({phone}): {message}', file=file)
#     return render(request, 'catalog/contacts.html', context)


class ContactsView(TemplateView):
    """
    Класс-контроллер для отображения страницы с контактами и обратной связью
    """

    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            name = self.request.POST.get('name')
            phone = self.request.POST.get('phone')
            message = self.request.POST.get('message')
            with open(ENTRY_PATH, "a", encoding="UTF-8") as file:
                print(f'You have new message from {name}({phone}): {message}', file=file)
        context_data['contact_data'] = Contact.objects.get(pk=2)
        return context_data


# def catalog(request: WSGIRequest) -> HttpResponse:
#     """
#     Контроллер для отображения страницы со списком всех товаров
#     """
#     context = {
#         'product_list': Product.objects.all(),
#     }
#     return render(request, 'catalog/catalog.html', context)


class ProductsListView(ListView):
    """
    Класс-контроллер для отображения страницы со списком всех товаров
    в порядке от новых к более старым
    """

    model = Product
    template_name = 'catalog/catalog.html'

    def get_queryset(self):
        return Product.objects.all().prefetch_related(
            Prefetch(
                'version_set',
                queryset=Version.objects.filter(status=True),
                to_attr='fetched_active_version'
            )
        ).order_by('-change_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context.get('product_list', [])

        for product in products:
            product.active_version = product.fetched_active_version[0] if product.fetched_active_version else None

        return context


# def category(request: WSGIRequest, pk: int) -> HttpResponse:
#     """
#     Контроллер для отображения страницы со списком товаров,
#     принадлежащих конкретной категории
#     """
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'product_list': Product.objects.filter(category_id=pk),
#         'title': category_item.name
#     }
#     return render(request, 'catalog/category.html', context)


class CategoryProductsListView(ListView):
    """
    Класс-контроллер для отображения страницы со списком товаров,
    принадлежащих конкретной категории
    """

    model = Product
    template_name = 'catalog/category.html'

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = Category.objects.get(pk=self.kwargs.get('pk'))
        return context_data


# def create_product(request: WSGIRequest) -> HttpResponse:
#     """
#     Контроллер для отображения страницы с карточкой описания нового товара.
#     После отправки этой информации товар будет создан и добавлен в базу данных,
#     если все обязательные поля заполнены
#     """
#     context = {
#         'category_list': Category.objects.order_by('pk'),
#     }
#     if request.method == "POST":
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         category = request.POST.get('category')
#         price = request.POST.get('price')
#         image = request.FILES.get('image', None)
#
#         creation_product = {
#             'name': name,
#             'description': description,
#             'category': Category.objects.get(pk=category),
#             'price': price,
#         }
#         if image:
#             creation_product['image'] = image
#         if all(creation_product.values()):
#             Product.objects.create(**creation_product)
#     return render(request, 'catalog/create_product.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-контроллер для отображения страницы с карточкой описания нового товара.
    После отправки этой информации товар будет создан и добавлен в базу данных,
    если все обязательные поля заполнены
    """

    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    extra_context = {
        'action': 'Создать'
    }
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


# def product(request: WSGIRequest, pk: int) -> HttpResponse:
#     """
#     Контроллер для отображения страницы с описанием конкретного товара
#     """
#     context = {
#         'product': Product.objects.get(pk=pk),
#     }
#     return render(request, 'catalog/product.html', context)


class ProductDetailView(DetailView):
    """
    Класс-контроллер для отображения страницы с описанием конкретного товара
    """

    model = Product
    template_name = 'catalog/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_version'] = Version.objects.filter(product=self.object, status=True).first()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс-контроллер для изменения карточки товара
    """

    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product,
                                               Version,
                                               form=VersionForm,
                                               extra=1,
                                               can_delete=False)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        extra_context = {
            'action': 'Изменить',
            'formset': formset,
        }
        return context_data | extra_context

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-контроллер для удаления товара
    """

    model = Product
    template_name = 'catalog/delete_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        extra_context = {
            'object': Product.objects.get(pk=self.kwargs.get('pk'))
        }
        return context_data | extra_context
