from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from users.forms import UserForm, LoginForm, UserRegisterForm
from users.models import User
import secrets
import users.services as services


class RegisterView(CreateView):
    """Класс-контроллер для регистрации нового пользователя"""

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:verify_message')
    template_name = 'users/registration.html'

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            verification_code = secrets.token_urlsafe(nbytes=7)
            instance.verification_code = verification_code

            url = reverse('users:verification', args=[verification_code])
            total_url = self.request.build_absolute_uri(url)
            services.send_verification_url(total_url, instance.email)

            instance.save()
        return super().form_valid(form)


class LoginView(BaseLoginView):
    """Класс-контроллер для реализации авторизации пользователя"""

    template_name = 'users/login.html'
    form_class = LoginForm


class VerifyMessage(TemplateView):
    """
    Класс-контроллер для выдачи предупреждающего сообщения
    о верификации пользователя по письму
    """

    template_name = 'users/verification_message.html'


def verification(request, verification_code):
    """
    Контроллер, реализующий механизм активации пользователя
    при переходе по ссылке из электронного письма
    """

    user = User.objects.get(verification_code=verification_code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    """Класс-контроллер для изменения профиля пользователя"""

    model = User
    template_name = 'users/profile.html'
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    """Контроллер для генерации нового пароля и отправки его на почту существующего пользователя"""

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден!')
        else:
            new_password = get_random_string(length=10)
            user.set_password(new_password)
            user.save()
            services.send_new_password(password=new_password, email=email)
            messages.success(request, 'На указанную почту был отправлен новый пароль!')

    return render(request, 'users/forget_password.html')