from django.urls import path
from django.conf.urls.static import static
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) #type: ignore

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register-user'),
    path('login/', TokenObtainPairView.as_view(), name='login-user'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh-user'),
    path('profile/', views.UserProfileView.as_view(), name='profile-user'),
]
