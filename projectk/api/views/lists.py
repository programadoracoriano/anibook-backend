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
from django.db.models import Avg, Sum, FloatField, F, Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
@authentication_classes([])
def AnimeListAPI(request):
    if request.method == 'GET':
        anime = Anime.objects.order_by("-id")[:4]
        serializer = AnimeSerializer(anime, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
def AnimeDetailsAPI(request):
    if request.method == 'GET':
        getId = request.GET['id']
        getAnime = Anime.objects.get(id=getId)
        serializer = AnimeSerializer(getAnime)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def PublicAnimeListAPI(request):
    if request.method == 'GET':
        status = request.GET['status']
        userId = request.GET['userId']
        serializer = ''
        if status == '0':
            getList = AnimeStatus.objects.filter(user__id=userId).order_by("status")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '1':
            getList = AnimeStatus.objects.filter(user__id=userId, status__val=1).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '2':
            getList = AnimeStatus.objects.filter(user__id=userId, status__val=2).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '3':
            getList = AnimeStatus.objects.filter(user__id=userId, status__val=5).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AnimeListAllAPI(request):
    if request.method == 'GET':
        status = request.GET['status']
        serializer = ''
        if status == '0':
            getList =  AnimeStatus.objects.filter(user=request.user).order_by("status")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '1':
            getList = AnimeStatus.objects.filter(user=request.user, status__val=1).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '2':
            getList = AnimeStatus.objects.filter(user=request.user, status__val=2).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '3':
            getList = AnimeStatus.objects.filter(user=request.user, status__val=5).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        msg = {}
        getAnime = Anime.objects.get(id=request.data['id'])
        anSt = AnimeStatus.objects.filter(anime=getAnime, user=request.user)
        if request.data['status'] == 1:
            n_episodes = int(request.data['ep_number'])
            if getAnime.episodes_number == None:
                getStatusWatching = Status.objects.get(val=1)
                query = AnimeStatus.objects.create(user=request.user, anime=getAnime,
                                                   status=getStatusWatching, episodes_number=n_episodes, completed=1)
                msg = {"msg": "Anime Added successfully"}
            elif anSt.count() == 0:
                if n_episodes == getAnime.episodes_number or n_episodes > getAnime.episodes_number:
                    getStatusCompleted = Status.objects.get(val=2)
                    query   = AnimeStatus.objects.create(user=request.user, anime=getAnime,
                                                         status=getStatusCompleted, completed=1)
                    msg     = {"msg":"Anime moved to completed section."}
                else:
                    getStatusWatching = Status.objects.get(val=1)
                    query = AnimeStatus.objects.create(user=request.user, anime=getAnime,
                                        status=getStatusWatching, episodes_number=n_episodes,completed=1)
                    msg = {"msg":"Anime Added successfully"}
            elif anSt.count() > 0:
                if n_episodes == getAnime.episodes_number or n_episodes > getAnime.episodes_number:
                    getStatusCompleted = Status.objects.get(val=2)
                    query = anSt.update(user=request.user, anime=getAnime, completed=1, status=getStatusCompleted,
                                        episodes_number=n_episodes)
                    msg = {"msg": "Anime moved to completed section."}
                else:
                    getStatusWatching = Status.objects.get(val=1)
                    anSt.update(episodes_number=n_episodes, status=getStatusWatching)
                    msg = {"msg": "Anime Updated successfully"}
            return Response(msg)
        if request.data['status'] == 2:
            if getAnime.episodes_number == None:
                msg = {"msg": "Anime can't be added to completed because it hasn't ended yet!"}
            elif anSt.count() == 0:
                getStatusCompleted = Status.objects.get(val=2)
                query = AnimeStatus.objects.create(user=request.user, anime=getAnime,
                                                   status=getStatusCompleted,
                                                   completed=request.data['completed'], score=request.data['score'])
                msg = {"msg":"Anime added successfully"}
            elif anSt.count() > 0:
                getStatusCompleted = Status.objects.get(val=2)
                query = anSt.update(user=request.user, anime=getAnime, status=getStatusCompleted,
                                    completed=request.data['completed'], episodes_number=0, score=request.data['score'])
                msg = {"msg":"Anime updated successfully"}
            return Response(msg)
        if request.data['status'] == 3:
            if anSt.count() == 0:
                getStatusPlanToWatch = Status.objects.get(val=5)
                query = AnimeStatus.objects.create(user=request.user, anime=getAnime, status=getStatusPlanToWatch)
                msg = {"msg":"Anime added to Plan to Watch."}
            elif anSt.count() > 0:
                msg = {"msg": "You are already watching, completed or dropped this anime!"}
            return Response(msg)
        if request.data['status'] == 4:
            if anSt.count() == 0:
                getStatusDropped = Status.objects.get(val=3)
                query = AnimeStatus.objects.create(user=request.user, anime=getAnime, status=getStatusDropped)
                msg = {"msg": "Anime added to Dropped"}
            elif anSt.count() > 0:
                getStatusDropped = Status.objects.get(val=3)
                query = anSt.update(user=request.user, anime=getAnime, status=getStatusDropped,
                                    completed=0, episodes_number=0, score=0)
                msg = {"msg": "Anime updated to dropped status!"}
            return Response(msg)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getStatusAPI(request):
    if request.method == 'GET':
        id          = request.GET['id']
        anime       = Anime.objects.get(id=id)
        qs          = AnimeStatus.objects.get(user=request.user, anime=anime)
        serializer  = AnimeStatusSerializer(qs, many=False)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AnimeNoteAPI(request):
    if request.method == 'GET':
        id = request.GET['note']
        serializer = ''
        if id is not None:
            qs          = AnimeStatus.objects.get(id=id)
            serializer = AnimeStatusSerializer(qs, many=False)
        return Response(serializer.data)
    if request.method == 'POST':
        note    = request.data['note']
        id      = request.data['id']
        msg     = {}
        if note is not None:
            qs  = AnimeStatus.objects.filter(id=id).update(note=note)
            msg = {"msg":"Note Updated Successfully"}
        else:
            msg = {"msg":"Note is Empty"}
        return Response(msg)

@api_view(['GET'])
@authentication_classes([])
def GetScoreAPI(request):
    if request.method == 'GET':
        anId            = request.GET['id']
        getAnime        = Anime.objects.annotate(total_score=Avg('animestatus__score', output_field=FloatField())).get(id=anId)
        tscore = {"total_score":getAnime.total_score}
        return Response(tscore)

@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
def CustomListAPI(request):
    if request.method == 'POST':
        title       = None
        mainA       = None
        msg         = {}
        serializer  = None
        if 'title' in request.data:
            title = request.data['title']
        if 'main' in request.data:
            mainA = request.data['main']
        if len(title) < 0 or len(title) > 100:
            msg = {{'msg':'You only can use 6 to 100 characters on title'}, {'msg':None}}
        elif mainA == None:
            msg = {{'msg': 'You Need to select a anime for thumbnail'}, {'msg':None}}
        else:
            getAnime        = Anime.objects.get(id=mainA)
            qs              = CustomList.objects.create(user=request.user, title=title, image=getAnime.image)
            query           = CustomList.objects.filter(user=request.user).order_by("-id")
            serializer      = CustomListSerializer(query, many=True)
            msg             = serializer.data
        return Response(msg)
    if request.method == 'GET':
        qs = CustomList.objects.filter(user=request.user).order_by("-id")
        serializer = CustomListSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def GetUniqueCustomList(request):
    if request.method == 'GET':
        cList = request.GET['id']
        qs = CustomList.objects.get(id=cList)
        serializer = CustomListSerializer(qs, many=False)
        return Response(serializer.data)


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
def AnimeCustomListAPI(request):
    if request.method == 'POST':
        cList       = request.data['id']
        animeId     = request.data['anime']
        getCList    = CustomList.objects.get(id=cList)
        getAnime    = Anime.objects.get(id=animeId)
        msg         = {}

        if cList == None:
            msg = {'msg':'Something Bad Happened!'}
        elif animeId == None:
            msg = {'msg': 'You need to choose a anime'}
        else:
            AnimeCustomList.objects.create(custom_list=getCList, anime=getAnime)
            msg = {'msg':'Anime Added Successfully!'}
        return Response(msg)
    if request.method == 'GET':
        customId = request.GET['id']
        qs = AnimeCustomList.objects.filter(custom_list__id=customId)
        serializer = AnimeCustomListSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
def PublicCustomListAPI(request):
    if request.method == 'GET':
        status = request.GET['status']
        qs = ''
        if status == '0':
            qs = CustomList.objects.order_by("?")[:4]
        elif status == '1':
            qs = CustomList.objects.order_by("-id")[:4]
        elif status == '2':
            user = request.GET['user']
            qs = CustomList.objects.filter(user__id=user)
        serializer = CustomListSerializer(qs, many=True)
        return Response(serializer.data)

#begin delete section
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def DeleteCustomListAPI(request):
    if request.method == 'GET':
        id = request.GET['id']
        qs = CustomList.objects.filter(id=request.GET['id'], user=request.user).delete()
        query = CustomList.objects.filter(user=request.user).order_by("-id")
        serializer = CustomListSerializer(query, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def DeleteItemFromListAPI(request):
    if request.method == 'GET':
        status      = request.GET['status']
        id          = request.GET['id']
        qs          = AnimeStatus.objects.filter(id=request.GET['id'], user=request.user).delete()
        serializer  = ''
        if status == '0':
            getList = AnimeStatus.objects.filter(user=request.user).order_by("status")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '1':
            getList = AnimeStatus.objects.filter(user=request.user, status__val=1).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '2':
            getList = AnimeStatus.objects.filter(user=request.user, status__val=2).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        elif status == '3':
            getList = AnimeStatus.objects.filter(user=request.user, status__val=5).order_by("-id")
            serializer = AnimeStatusSerializer(getList, many=True)
        return Response(serializer.data)