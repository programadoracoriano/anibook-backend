from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from api.views import *


urlpatterns = [

    path('search/user/', UserSearchAPI, name="usersearch"),
    path('search/all/', AnimeSearchAPI, name="search"),
    path('search/by/season/', SeasonSearchAPI, name="searchseason"),
    path('search/by/genre/', SearchByGenreAPI, name="searchbygenre"),
    path('search/anime/list/', AnimeListSearchAPI, name="animelistsearch"),
    path('get/genres/', GetGenresAPI, name="getgenres"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
