from typing import Any

from common.mixins import CommonContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'wishlists/index.html'
    title = 'Wheesh'


class WishlistView(CommonContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'wishlists/wishlist.html'
    title = 'Мой вишлист'
