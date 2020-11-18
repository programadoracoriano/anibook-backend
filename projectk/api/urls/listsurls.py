from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from api.views import *

urlpatterns = [
    path('customlist/', CustomListAPI, name="customlist"),
    path('anime/customlist/', AnimeCustomListAPI, name="animecustomlist"),
    path('get/public/customlist/', PublicCustomListAPI, name="publiccustomlist"),
    path('get/unique/customlist/', GetUniqueCustomList, name="ucustomlist"),
    path('list/public/anime/', PublicAnimeListAPI, name="listpublicanime"),
    path('get/anime/list/', AnimeListAPI, name="listanimes"),
    path('get/anime/details/', AnimeDetailsAPI, name="animedetails"),
    path('get/anime/score/', GetScoreAPI, name="animescore"),
    path('anime/list/all/', AnimeListAllAPI, name="allanimelist"),
    path('anime/note/', AnimeNoteAPI, name="animenote"),
    path('get/anime/status/', getStatusAPI, name="statusapi"),

    #Delete Urls
    path('delete/customlist/', DeleteCustomListAPI, name="deletecustomlist"),
    path('delete/anime/customlist/', DeleteAnimeCustomListAPI, name="deleteanimecustomlist"),
    path('delete/anime/list/', DeleteItemFromListAPI, name="deleteanimefromlist"),

    #token
    path('api-token-auth/', views.obtain_auth_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)