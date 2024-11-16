from django.urls import path

from .views import WishlistView

app_name = 'wishlists'

urlpatterns = [
    path('', WishlistView.as_view(), name='personal'),
]
