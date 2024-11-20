from django.urls import path

from .views import NewPresentView, WishlistView

app_name = 'wishlists'

urlpatterns = [
    path('', WishlistView.as_view(), name='personal'),
    path('present/new/', NewPresentView.as_view(), name='new_item'),
]
