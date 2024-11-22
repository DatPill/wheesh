from django.urls import path

from .views import DeletePresentView, EditPresentView, NewPresentView, WishlistView

app_name = 'wishlists'

urlpatterns = [
    path('', WishlistView.as_view(), name='personal'),
    path('present/new/', NewPresentView.as_view(), name='new_item'),
    path('present/<int:pk>/edit/', EditPresentView.as_view(), name='edit_item'),
    path('present/<int:pk>/delete/', DeletePresentView.as_view(), name='delete_item'),
]
