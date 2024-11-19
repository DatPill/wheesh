from typing import Any

from common.mixins import CommonContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from wishlists.models import Wishlist

from .models import User


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    title = 'Wheesh - Регистрация'
    form_class = UserRegistrationForm
    model = User
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались!'


    def form_valid(self, form):
        user = form.save()
        Wishlist.objects.create(title='Основной вишлист', user=user)
        return super().form_valid(form)


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    title = 'Wheesh - Вход'
    next_page = '/'
    form_class = UserLoginForm
    model = User


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = '/'


class UserProfileView(CommonContextMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    title = 'Wheesh - Профиль'
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')


    def get_object(self) -> Model:
        return self.model.objects.get(pk=self.request.user.pk)


    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = super().get_form_kwargs()

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )

        return kwargs
