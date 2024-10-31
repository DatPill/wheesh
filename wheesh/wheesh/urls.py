from django.contrib import admin
from django.urls import include, path
from wishlists.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('wishlists/', include('wishlists.urls', namespace='wishlists')),
]
