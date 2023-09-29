from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from blog.services import send_congratulatory_email
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from blog.models import BlogEntry
from pytils.translit import slugify

# Create your views here.


class BlogEntryListView(ListView):
    """
    Класс-контроллер для отображения страницы со списком публикаций блога
    """

    model = BlogEntry
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        object_list = BlogEntry.objects.filter(is_published=True)
        object_list = object_list.order_by('-creation_date')
        context_data['object_list'] = object_list
        context_data['button_text'] = 'Разопубликовать'
        return context_data


class BlogEntryCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-контроллер для отображения формы создания новой публикации блога
    """

    model = BlogEntry
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:unpublished_entries')
    template_name = 'blog/form_blog_entry.html'
    extra_context = {
        'action': 'Создать',
    }

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.slug = slugify(self.object.title)
            self.object.author = self.request.user
            self.object.save()
            return super().form_valid(form)


class BlogEntryUnpublishedListView(LoginRequiredMixin, BlogEntryListView):
    """
    Класс-контроллер для отображения страницы со списком неопубликованных записей блога
    """

    model = BlogEntry
    template_name = 'blog/unpublished_entries.html'

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        object_list = BlogEntry.objects.filter(is_published=False)

        if not self.request.user.is_superuser:
            object_list = object_list.filter(author=self.request.user)

        object_list = object_list.order_by('-creation_date')
        context_data['object_list'] = object_list
        context_data['button_text'] = 'Опубликовать'
        return context_data


class BlogEntryDetailView(DetailView):
    """
    Класс-контроллер для отображения страницы с конкретной записью блога
    """

    model = BlogEntry
    template_name = 'blog/current_blog_entry.html'

    def get_object(self, queryset=None) -> QuerySet:
        self.object = super().get_object(queryset)
        if self.object.is_published:
            self.object.number_views += 1
            self.object.save()
        if self.object.number_views == 100:
            send_congratulatory_email(self.object)
        return self.object

@login_required
def publish_blog_entry(request, slug):
    """
    Контроллер для изменения статуса публикации
    (is_published: True/False)
    """

    blog_entry = get_object_or_404(BlogEntry, slug=slug)
    redirect_url = 'blog:blog' if blog_entry.is_published else 'blog:unpublished_entries'
    blog_entry.is_published = not blog_entry.is_published
    blog_entry.save()

    return redirect(redirect_url)


class BlogEntryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс-контроллер для изменения записи блога
    """

    model = BlogEntry
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:unpublished_entries')
    template_name = 'blog/form_blog_entry.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        extra_context = {
            'action': 'Сохранить',
            'object': BlogEntry.objects.get(slug=self.kwargs.get('slug'))
        }
        return context_data | extra_context


class BlogEntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-контроллер для удаления записи блога
    """

    model = BlogEntry
    template_name = 'blog/delete_entry.html'
    success_url = reverse_lazy('blog:unpublished_entries')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user or not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        extra_context = {
            'object': BlogEntry.objects.get(slug=self.kwargs.get('slug'))
        }
        return context_data | extra_context