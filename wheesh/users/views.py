from typing import Any

from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

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


class UserProfileView(UpdateView):
    template_name = 'users/profile.html'
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')


    def get_object(self) -> Model:
        return self.model.objects.get(pk=self.request.user.pk)


    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )

        return kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['title'] = 'Wheesh - Профиль'

        return context
