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
def SignupAPI(request):
    if request.method == 'POST':
        msg = {}
        username = request.data['username']
        password = request.data['password']
        getUsers = User.objects.filter(username=username)
        if getUsers.count() > 0:
            msg = {'msg':'User Already Exists!Please choose other username!', 'success':False}
        elif len(username) < 6 or len(username)> 20:
            msg = {'msg': 'Your username needs to be 6 to 20 characters.', 'success':False}
        elif len(password) < 8 or len(password)>16:
            msg = {'msg': 'Your passwords needs to be 8 to 16 characters.', 'success':False}
        else:
            qs = User.objects.create_user(username=username, password=password)
            msg = {'msg': 'User created successfully!', 'success':True}
        return Response(msg)


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

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def DefaulAvatarAPI(request):
    if request.method == 'GET':
        getAv = DefaultAvatar.objects.order_by("id")
        serializer = DefaultAvatarSerializer(getAv, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        avId = request.data['avatar']
        instanceAv = DefaultAvatar.objects.get(id=avId)
        msg = {}
        if avId == None:
            msg = {"msg":"No Avatar has been Selected"}
        else:
            qs = Profile.objects.filter(user=request.user).update(image=instanceAv.image)
            msg = {"msg": "Avatar Changed Successfully!"}
        return Response(msg)

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
def FollowerAPI(request):
    if request.method == 'GET':
        followerId      = request.GET['id']
        followers       = Followers.objects.filter(follower=request.user, followers=followerId)
        f_state         = 0
        if followers.count() == 0:
            qs = Followers.objects.create(follower=request.user, followers=followerId)
            f_state = 0
        elif followers.count() > 0:
            qs = Followers.objects.filter(follower=request.user, followers=followerId).delete()
            f_state = 1
        return Response({"f_state":f_state})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def DetectFollowerAPI(request):
    followerId = request.GET['id']
    followers = Followers.objects.filter(follower=request.user, followers=followerId)
    f_state = 0
    if followers.count() == 0:
        f_state = 1
    elif followers.count() > 0:
        f_state = 0
    return Response({"f_state": f_state})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ListFollowersAPI(request):
    if request.method == 'GET':
        followersList = []
        follower = ''
        getF = Followers.objects.filter(follower=request.user)
        for i in getF:
            followersList.append(i.followers)
        qs = User.objects.filter(id__in=followersList)
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 15)
        try:
            follower = paginator.page(page)
        except PageNotAnInteger:
            follower = paginator.page(1)
        except EmptyPage:
            follower = paginator.page(paginator.num_pages)
        serializer = UserSerializer(follower, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ListFollowingAPI(request):
    if request.method == 'GET':
        follower = ''
        qs = Followers.objects.filter(followers=request.user.id)
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 15)
        try:
            follower = paginator.page(page)
        except PageNotAnInteger:
            follower = paginator.page(1)
        except EmptyPage:
            follower = paginator.page(paginator.num_pages)
        serializer = FollowerSerializer(follower, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AnimeReviewAPI(request):
    if request.method == 'GET':
        id = request.GET['id']
        qs = AnimeReview.objects.filter(anime__id=id)
        serializer = AnimeReviewSerializer(qs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        id  = request.data['id']
        rev = request.data['review']
        msg = {}
        if rev is not None:
            anime       = Anime.objects.get(id=id)
            qs          = AnimeReview.objects.create(anime=anime, user=request.user, review=rev)
            msg         = {"msg":"Review Added Successfully"}
        else:
            msg = {"msg": "You need to write a review!"}
        return Response(msg)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def LogoutAPI(request):
    return Response({"isLoggout":True})