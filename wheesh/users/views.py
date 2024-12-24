from typing import Any

from common.mixins import CommonContextMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.base import Model
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User
from users.utils import (
    create_verification_object,
    email_verification_service,
    generate_verification_code,
)
from wishlists.models import Wishlist


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    title = 'Wheesh - Регистрация'
    form_class = UserRegistrationForm
    model = User
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались!\nОбязательно подтвердите свою электронную почту перед входом!'

    def form_valid(self, form):
        user = form.save(is_final=False)
        Wishlist.objects.create(title='Основной вишлист', user=user)
        return super().form_valid(form)


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    title = 'Wheesh - Вход'
    next_page = '/'
    form_class = UserLoginForm
    model = User

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.email_verified:
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                messages.warning(self.request, "Сначала подтвердите свою почту, перейдя по ссылке в письме!")
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


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


class EmailVerificationView(CommonContextMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        email = kwargs['email']
        user = User.objects.get(email=email)
        email_verification = EmailVerification.objects.filter(code=code, user=user)
        verification_expired = email_verification.last().is_expired()

        if email_verification.exists():
            if not verification_expired:
                user.email_verified = True
                user.save()
                return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('users:verification_expired', args=(email, code)))

        else:
            return HttpResponseNotFound('Такой ссылки не существует')


class VerificationExpiredView(CommonContextMixin, SuccessMessageMixin, TemplateView):
    title = 'Ссылка недействительна'
    template_name = 'users/verification_expired.html'

    def get(self, request, *args, **kwargs):
        email = kwargs['email']
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.last()
            if user.email_verified:
                return HttpResponseRedirect(reverse('users:profile'))

            code = generate_verification_code()
            create_verification_object(user.id, code)
            email_verification_service.send_verification_web(user.id, user.email, user.username, code)
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseNotFound('Такой ссылки не существует')
