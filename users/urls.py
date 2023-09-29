from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, LoginView, verification, VerifyMessage, UserUpdateView, generate_new_password
from django.views.decorators.cache import never_cache

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', never_cache(RegisterView.as_view()), name='registration'),
    path('verify_message/', never_cache(VerifyMessage.as_view()), name='verify_message'),
    path('', never_cache(LoginView.as_view()), name='login'),
    path('logout/', never_cache(LogoutView.as_view()), name='logout'),
    path('logout/genpassword/', never_cache(generate_new_password), name='new_password'),
    path('verification/<str:verification_code>', never_cache(verification), name='verification'),
    path('profile/', never_cache(UserUpdateView.as_view()), name='profile'),
]