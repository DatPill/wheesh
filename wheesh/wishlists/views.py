from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.db.models.query import Q, QuerySet
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from common.mixins import CommonContextMixin, OwnershipRequiredMixin
from wishlists.forms import EditPresentForm, NewPresentForm
from wishlists.models import Present, Wishlist


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'wishlists/index.html'
    title = 'Wheesh'


class PersonalWishlistView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/personal_wishlist.html'
    model = Wishlist
    context_object_name = 'wishlist'
    title = 'Мой вишлист - Wheesh'

    def get_queryset(self) -> QuerySet[Any]:
        wishlist = Wishlist.objects.filter(Q(user_id=self.request.user.id) & Q(title='Основной вишлист'))
        if wishlist.exists():
            self.__wishlist = wishlist.first()
            presents_queryset = self.__wishlist.presents.all().order_by('-pk')

            return presents_queryset

        self.__wishlist = Wishlist.objects.none()
        return self.__wishlist


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_instance'] = self.__wishlist

        return context


class WishlistView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/wishlist.html'
    model = Wishlist
    context_object_name = 'wishlist'

    def get(self, request, *args, **kwargs):
        wishlist = Wishlist.objects.filter(slug_url=self.kwargs['wishlist_slug'])
        if wishlist.exists():
            self.__wishlist = wishlist.first()
            if self.__wishlist.user == self.request.user:
                return redirect('wishlists:personal')

            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseNotFound('Такого вишлиста не существует ( ._.\')')

    def get_queryset(self) -> QuerySet[Any]:
        self.title = f'{self.__wishlist.user.username} - {self.__wishlist.title}'
        presents_queryset = self.__wishlist.presents.order_by('-pk')

        return presents_queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_instance'] = self.__wishlist

        return context


class NewPresentView(CommonContextMixin, LoginRequiredMixin, CreateView):
    template_name = 'wishlists/new_item.html'
    title = 'Добавить новый подарок - Wheesh'
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
    title = 'Изменить подарок - Wheesh'
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


class ManagePresentReservationView(View):
    def get(self, request, present_id):  # TODO: make it POST request
        present = Present.objects.filter(pk=present_id)

        if present.exists():
            present = present.first()

            if present.reserved_by:
                present.reserved_by = None
            else:
                present.reserved_by = request.user

            present.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseNotFound('Такого подарка не существует')


class ReservationsView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/reservations.html'
    title = 'Я дарю - Wheesh'
    model = Present
    context_object_name = 'wishlists'

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user

        return Wishlist.objects.filter(presents__reserved_by=user).distinct().prefetch_related(
            Prefetch(
                'presents',
                queryset=Present.objects.filter(reserved_by=user),
                to_attr='reserved_presents'
            )
        )
