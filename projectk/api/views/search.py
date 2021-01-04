from rest_framework.authentication import TokenAuthentication, SessionAuthentication
#from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView

from ..models import *
from ..serializers import *
from django.db.models import Avg, Sum, FloatField, F, Count, Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
@authentication_classes([])
def AnimeSearchAPI(request):
    if request.method == 'GET':
        anime = Anime.objects.filter(name__icontains=str(request.GET['search'])) | \
                                     Anime.objects.filter(alternative_title__title__icontains=str(request.GET['search']))
        cquery = anime.order_by("name").distinct()
        serializer = AnimeSerializer(cquery, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
def GetGenresAPI(request):
    if request.method == 'GET':
        qs = Categorie.objects.order_by("categorie")
        serializer = CategorieSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
def SearchByGenreAPI(request):
    if request.method == 'GET':
        genre   = request.GET['genre']
        qs      = Anime.objects.filter(categorie__id=genre)
        serializer = AnimeSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
def SeasonSearchAPI(request):
    if request.method == 'GET':
        winter = ['01', '02', '03']
        spring = ['04', '05', '06']
        summer = ['07', '08', '09']
        fall = ['10', '11', '12']
        anime = None
        season = request.GET['season']
        year = request.GET['year']
        if season == 'winter':
            anime = Anime.objects.filter(aired__month__in=winter, aired__year=year).order_by("?")
        elif season == 'spring':
            anime = Anime.objects.filter(aired__month__in=spring, aired__year=year).order_by("?")
        elif season == 'summer':
            anime = Anime.objects.filter(aired__month__in=summer, aired__year=year).order_by("?")
        elif season == 'fall':
            anime = Anime.objects.filter(aired__month__in=fall, aired__year=year).order_by("?")
        serializer = AnimeSerializer(anime, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserSearchAPI(request):
    if request.method == 'GET':
        search      = request.GET['search']
        query       = User.objects.filter(username__icontains=search)
        serializer  = UserSerializer(query, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def AnimeListSearchAPI(request):
    if request.method == 'GET':
        search = request.GET['search']
        query = AnimeStatus.objects.filter(anime__name__icontains=search, user=request.user)
        serializer = AnimeStatusSerializer(query, many=True)
        return Response(serializer.data)