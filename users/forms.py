from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from users.models import User


class StyleFormMixin:
    """Класс-миксин для примешивания стилей"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: center;'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """ Форма для регистрации пользователя """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None


class LoginForm(StyleFormMixin, AuthenticationForm):
    """ Форма для аутентификации пользователя """

    pass


class UserForm(StyleFormMixin, UserChangeForm):
    """ Форма для изменения профиля пользователя """

    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()