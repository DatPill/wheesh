from typing import Any

from common.mixins import CommonContextMixin, OwnershipRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Q, QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import EditPresentForm, NewPresentForm
from .models import Present, Wishlist


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'wishlists/index.html'
    title = 'Wheesh'


class PersonalWishlistView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/personal_wishlist.html'
    model = Wishlist
    context_object_name = 'wishlist'
    title = 'Мой вишлист'

    def get_queryset(self) -> QuerySet[Any]:
        self.__wishlist = get_object_or_404(Wishlist, Q(user_id=self.request.user.id) & Q(title='Основной вишлист'))
        presents_queryset = self.__wishlist.presents.all().order_by('-pk')

        return presents_queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_instance'] = self.__wishlist

        return context


class WishlistView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/wishlist.html'
    model = Wishlist
    context_object_name = 'wishlist'


    def get(self, request, *args, **kwargs):
        self.__wishlist = get_object_or_404(Wishlist, slug_url=self.kwargs['wishlist_slug'])

        if self.__wishlist.user == self.request.user:
            return redirect('wishlists:personal')

        return super().get(request, *args, **kwargs)


    def get_queryset(self) -> QuerySet[Any]:
        self.title = f'{self.__wishlist.user.username} - {self.__wishlist.title}'
        presents_queryset = self.__wishlist.presents.filter(Q(reserved_by=None) | Q(reserved_by=self.request.user)).order_by('-pk')

        return presents_queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_instance'] = self.__wishlist

        return context


class NewPresentView(CommonContextMixin, LoginRequiredMixin, CreateView):
    template_name = 'wishlists/new_item.html'
    title = 'Добавить новый подарок'
    form_class = NewPresentForm
    model = Present
    success_url = reverse_lazy('wishlists:personal')

    def form_valid(self, form):
        present = form.save(commit=False)
        user = self.request.user

        present.wishlist = Wishlist.objects.get(Q(user_id=self.request.user.id) & Q(title='Основной вишлист'))
        present.user = user
        present.save()

        return super().form_valid(form)

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


class EditPresentView(OwnershipRequiredMixin, CommonContextMixin, UpdateView):
    template_name = 'wishlists/edit_item.html'
    title = 'Изменить подарок'
    form_class = EditPresentForm
    model = Present
    success_url = reverse_lazy('wishlists:personal')
    forbidden_message = 'Вы не можете редактировать этот подарок'


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


class DeletePresentView(OwnershipRequiredMixin, CommonContextMixin, DeleteView):
    model = Present
    success_url = reverse_lazy('wishlists:personal')
    forbidden_message = 'Вы не можете удалить этот подарок'
