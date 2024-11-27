from django.urls import path

from .views import (
    DeletePresentView,
    EditPresentView,
    NewPresentView,
    PersonalWishlistView,
    WishlistView,
)

app_name = 'wishlists'

urlpatterns = [
    path('personal/', PersonalWishlistView.as_view(), name='personal'),
    path('<str:wishlist_slug>/', WishlistView.as_view(), name='other'),
    path('personal/present/new/', NewPresentView.as_view(), name='new_item'),
    path('personal/present/<int:pk>/edit/', EditPresentView.as_view(), name='edit_item'),
    path('personal/present/<int:pk>/delete/', DeletePresentView.as_view(), name='delete_item'),
]
