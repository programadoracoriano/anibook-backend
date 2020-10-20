"""projectk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/user/', SignupAPI, name="signup"),
    path('login/user/', LoginAPI, name="signin"),
    path('login/guard/', LoginGuardAPI, name="loginguard"),
    re_path(r'^update/profile/(?P<filename>[^/]+)$', ChangeProfileImageAPI.as_view(), name="changeprofileimage"),
    path('logout/', LogoutAPI, name="logout"),
    path('get/user/profile/', UserDetailsAPI, name="userdetails"),
    path('get/user/profile/extra/', UserExtraDetailsAPI, name="userextradetails"),
    path('get/profile/', ProfileAPI, name="getprofile"),
    path('get/user/data/', UserDataAPI, name="getuserdata"),
    path('get/follower/', FollowerAPI, name="followers"),
    path('detect/follower/', DetectFollowerAPI, name="detectfollower"),
    path('list/followers/', ListFollowersAPI, name="listfollower"),
    path('list/following/', ListFollowingAPI, name="listfollowing"),
    path('search/user/', UserSearchAPI, name="usersearch"),
    path('customlist/', CustomListAPI, name="customlist"),
    path('anime/customlist/', AnimeCustomListAPI, name="animecustomlist"),
    path('get/unique/customlist/', GetUniqueCustomList, name="ucustomlist"),
    path('get/anime/list/', AnimeListAPI, name="listanimes"),
    path('get/anime/details/', AnimeDetailsAPI, name="animedetails"),
    path('get/anime/score/', GetScoreAPI, name="animescore"),
    path('anime/list/all/', AnimeListAllAPI, name="allanimelist"),
    path('search/all/', AnimeSearchAPI, name="search"),
    path('search/by/season/', SeasonSearchAPI, name="searchseason"),
    path('search/by/genre/', SearchByGenreAPI, name="searchbygenre"),
    path('get/genres/', GetGenresAPI, name="getgenres"),
    path('api-token-auth/', views.obtain_auth_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
