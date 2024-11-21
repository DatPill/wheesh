from typing import Any

from common.mixins import CommonContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import NewPresentForm
from .models import Present, Wishlist


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'wishlists/index.html'
    title = 'Wheesh'


class WishlistView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = 'wishlists/wishlist.html'
    model = Present
    context_object_name = 'wishlist'
    title = 'Мой вишлист'

    def get_queryset(self) -> QuerySet[Any]:
        wishlist = Wishlist.objects.get(title='Основной вишлист').presents.all().order_by('-pk')

        return wishlist


class NewPresentView(CommonContextMixin, LoginRequiredMixin, CreateView):
    template_name = 'wishlists/new_item.html'
    title = 'Добавить новый подарок'
    form_class = NewPresentForm
    model = Present
    success_url = reverse_lazy('wishlists:personal')

    def form_valid(self, form):
        present = form.save(commit=False)
        user = self.request.user

        present.wishlist = Wishlist.objects.get(title='Основной вишлист')
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
