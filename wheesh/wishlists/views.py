from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'wishlists/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)

        context['title'] = 'Wheesh'
        return context

class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'wishlists/wishlist.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)

        context['title'] = 'Мой вишлист'
        return context
