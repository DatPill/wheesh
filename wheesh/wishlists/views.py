from typing import Any

from common.mixins import CommonContextMixin, OwnershipRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Q, QuerySet
from django.shortcuts import get_object_or_404
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
        presents_queryset = Wishlist.objects.get(Q(user_id=self.request.user.id) & Q(title='Основной вишлист')).presents.all().order_by('-pk')

        return presents_queryset


class WishlistView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/wishlist.html'
    model = Wishlist
    context_object_name = 'wishlist'


    def get_queryset(self) -> QuerySet[Any]:
        __wishlist = get_object_or_404(Wishlist, slug_url=self.kwargs['wishlist_slug'])
        self.title = f'{__wishlist.user.username} - {__wishlist.title}'
        presents_queryset = __wishlist.presents.filter(Q(reserved_by=None) | Q(reserved_by=self.request.user)).order_by('-pk')

        return presents_queryset


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
