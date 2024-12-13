from django.urls import path

from .views import (
    DeletePresentView,
    EditPresentView,
    ManagePresentReservationView,
    NewPresentView,
    PersonalWishlistView,
    ReservationsView,
    WishlistView,
)

app_name = 'wishlists'

urlpatterns = [
    path('personal/', PersonalWishlistView.as_view(), name='personal'),
    path('reserved/', ReservationsView.as_view(), name='reservations'),
    path('<str:wishlist_slug>/', WishlistView.as_view(), name='other'),
    path('personal/present/new/', NewPresentView.as_view(), name='new_item'),
    path('personal/present/<int:pk>/edit/', EditPresentView.as_view(), name='edit_item'),
    path('personal/present/<int:pk>/delete/', DeletePresentView.as_view(), name='delete_item'),
    path('present/<int:present_id>/reserve', ManagePresentReservationView.as_view(), name='manage_reservation'),
]
