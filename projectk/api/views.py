from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from django.db.models import Avg, Sum, FloatField, F, Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@api_view(['GET'])
@authentication_classes([])
def LoginGuardAPI(request):
    if request.method == 'GET':
        tk      = request.GET['tk']
        count_u = User.objects.filter(auth_token=tk).count()
        if count_u == 0:
            isLogged = False
        elif count_u > 0:
            isLogged = True
        return Response({"isLogged":isLogged})



@api_view(['POST'])
@authentication_classes([])
def LoginAPI(request):            # <-- And here
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        content = {}
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            print(token[0])

            content = {'token': str(token[0]), 'msg':'You have successfully logged!', 'success':True}
        else:
            content = {'msg':'Username or password are wrong!', 'success':False}
        return Response(content)

    elif request.method == 'POST':
        content = {}
        username = request.data['username']
        password = request.data['password']
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(username=username, password=password)
            message = {"msg":"You have successfully Registered!"}
        else:
            message = {"msg": "Some error has occured"}
        return Response(content)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserDetailsAPI(request):
    if request.method == 'GET':
        uId         = request.GET['id']
        user        = User.objects.get(id=uId)
        serializer  = UserSerializer(user)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserExtraDetailsAPI(request):
    if request.method == 'GET':
        uId = request.GET['id']
        u = User.objects.get(id=uId)
        user = User.objects.annotate(total_watching=Sum(F('animestatus__episodes_number') * F('animestatus__anime__episodes_number'), output_field=FloatField()) /60,
                                     total_completed=Sum((F('animestatus__completed') * F('animestatus__anime__episodes_number')) * F('animestatus__anime__minutes_per_episode'),
                                                         output_field=FloatField())/ 60).get(id=u.id)
        total_completed = AnimeStatus.objects.filter(user=u, status__id=2).count()
        total_watching = AnimeStatus.objects.filter(user=u, status__id=1).count()
        return Response({"total_hours":user.total_watching,
                         "total_completed":user.total_completed,
                         "animes_completed":total_completed,
                         "animes_watching":total_watching})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ProfileAPI(request):
    if request.method == 'GET':
        getUser = User.objects.get(id=request.user.id)
        serializer = UserSerializer(getUser, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserDataAPI(request):
    if request.method == 'GET':
        user = User.objects.annotate(total_watching=Sum(F('animestatus__episodes_number') * F('animestatus__anime__episodes_number'), output_field=FloatField()) /60,
                                     total_completed=Sum((F('animestatus__completed') * F('animestatus__anime__episodes_number')) * F('animestatus__anime__minutes_per_episode'),
                                                         output_field=FloatField())/ 60).get(id=request.user.id)
        total_completed = AnimeStatus.objects.filter(user=request.user, status__id=2).count()
        total_watching = AnimeStatus.objects.filter(user=request.user, status__id=1).count()
        return Response({"total_hours":user.total_watching,
                         "total_completed":user.total_completed,
                         "animes_completed":total_completed,
                         "animes_watching":total_watching})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def LogoutAPI(request):
    return Response({"isLoggout":True})

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

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AnimeListAllAPI(request):
    if request.method == 'GET':
        status = request.GET['status']
        serializer = ''
        if status == '0':
            getList =  AnimeStatus.objects.filter(user=request.user).order_by("status")
            serializer = AnimeStatusSerializer(getList, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        msg = {}
        getAnime = Anime.objects.get(id=request.data['id'])
        anSt = AnimeStatus.objects.filter(anime=getAnime, user=request.user)
        if request.data['status'] == 1:
            n_episodes = int(request.data['ep_number'])
            if anSt.count() == 0:
                if n_episodes == getAnime.episodes_number or n_episodes > getAnime.episodes_number:
                    getStatusCompleted = Status.objects.get(val=2)
                    query   = AnimeStatus.objects.create(user=request.user, anime=getAnime,
                                                         status=getStatusCompleted, completed=1)
                    msg     = {"msg":"Anime moved to completed section."}
                else:
                    getStatusWatching = Status.objects.get(val=1)
                    query = AnimeStatus.objects.create(user=request.user, anime=getAnime,
                                        status=getStatusWatching, completed=1)
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
            if anSt.count() == 0:
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



@api_view(['GET'])
@authentication_classes([])
def AnimeSearchAPI(request):
    if request.method == 'GET':
        anime = Anime.objects.filter(name__icontains=request.GET['search'])
        page = request.GET.get('page', 1)
        paginator = Paginator(anime, 15)
        try:
            animes = paginator.page(page)
        except PageNotAnInteger:
            animes = paginator.page(1)
        except EmptyPage:
            animes = paginator.page(paginator.num_pages)
        serializer = AnimeSerializer(animes, many=True)
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
        qs      = Anime.objects.filter(categorie__in=genre)
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 15)
        try:
            animes = paginator.page(page)
        except PageNotAnInteger:
            animes = paginator.page(1)
        except EmptyPage:
            animes = paginator.page(paginator.num_pages)
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
def SeasonSearchAPI(request):
    if request.method == 'GET':
        winter = ['01', '02', '03']
        spring = ['04', '05', '06']
        summer = ['07', '08', '09']
        fall = ['10', '11', '12']
        anime = ''
        season = request.GET['season']
        year = request.GET['year']
        if season == 'winter':
            anime = Anime.objects.filter(aired__month__in=winter, aired__year=year)
        elif season == 'spring':
            anime = Anime.objects.filter(aired__month__in=spring, aired__year=year)
        elif season == 'summer':
            anime = Anime.objects.filter(aired__month__in=summer, aired__year=year)
        elif season == 'fall':
            anime = Anime.objects.filter(aired__month__in=fall, aired__year=year)
        page = request.GET.get('page', 1)
        paginator = Paginator(anime, 15)
        try:
            animes = paginator.page(page)
        except PageNotAnInteger:
            animes = paginator.page(1)
        except EmptyPage:
            animes = paginator.page(paginator.num_pages)
        serializer = AnimeSerializer(animes, many=True)
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
@authentication_classes([])
def GetScoreAPI(request):
    if request.method == 'GET':
        anId            = request.GET['id']
        getAnime        = Anime.objects.annotate(total_score=Avg('animestatus__score', output_field=FloatField())).get(id=anId)
        tscore = {"total_score":getAnime.total_score}
        return Response(tscore)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def FollowerAPI(request):
    if request.method == 'GET':
        followerId      = request.GET['id']
        followers       = Followers.objects.filter(follower=request.user, followers=followerId)
        f_state         = 0
        print(request.user.username)
        if followers.count() == 0:
            qs = Followers.objects.create(follower=request.user, followers=followerId)
            f_state = 1
        elif followers.count > 0:
            qs = Followers.objects.delete()
            f_state = 0
        return Response({"f_state":f_state})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def DetectFollowerAPI(request):
    followerId = request.GET['id']
    followers = Followers.objects.filter(follower=request.user, followers=followerId)
    f_state = 0
    if followers.count() == 0:
        f_state = 1
    elif followers.count > 0:
        f_state = 0
    return Response({"f_state": f_state})









