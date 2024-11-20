from common.mixins import CommonContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import NewPresentForm
from .models import Present, Wishlist


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'wishlists/index.html'
    title = 'Wheesh'


class WishlistView(CommonContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'wishlists/wishlist.html'
    title = 'Мой вишлист'


class NewPresentView(CommonContextMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'wishlists/new_item.html'
    title = 'Добавить новый подарок'
    form_class = NewPresentForm
    model = Present
    success_url = reverse_lazy('wishlists:personal')
    success_message = 'Подарок успешно добавлен!'

    def form_valid(self, form):
        present = form.save(commit=False)
        user = self.request.user

        present.wishlist = Wishlist.objects.get(user=user)
        present.user = user
        present.save()

        return super().form_valid(form)
