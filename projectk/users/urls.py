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
    path('profile/create/', views.CreateUserProfileView.as_view(), name='profile-user'),
    path('profile/update/', views.UpdateUserProfileView.as_view(), name='update-profile-user'),
    path('profile/retrieve/', views.RetrieveUserProfileView.as_view(), name='retrieve-profile-user'),
]
