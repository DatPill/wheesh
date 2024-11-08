from typing import Any

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from users.forms import UserLoginForm, UserRegistrationForm

from .models import User


class UserRegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    model = User
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['title'] = 'Wheesh - Регистрация'

        return context

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = '/'
    form_class = UserLoginForm
    model = User

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['title'] = 'Wheesh - Вход'

        return context


class UserLogoutView(LogoutView):
    next_page = '/'
