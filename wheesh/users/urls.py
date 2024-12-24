from django.urls import path
from users.views import (
    EmailVerificationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserRegistrationView,
    VerificationExpiredView,
)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify/<str:email>/<int:code>/', EmailVerificationView.as_view(), name='verify'),
    path('expired/<str:email>/<int:code>/', VerificationExpiredView.as_view(), name='verification_expired'),
]
