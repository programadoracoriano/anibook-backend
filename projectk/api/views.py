from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

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



@api_view(['GET'])
@authentication_classes([])
def LoginAPI(request):            # <-- And here
    if request.method == 'GET':
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
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
def ProfileAPI(request):
    if request.method == 'GET':
        getUser = User.objects.get(id=request.user.id)
        serializer = UserSerializer(getUser, many=False)
        return Response(serializer.data)





@api_view(['GET'])
@authentication_classes([])
def LogoutAPI(request):
    return Response({"isLoggout":True})

@api_view(['GET'])
@authentication_classes([])
def AnimeListAPI(request):
    if request.method == 'GET':
        anime = Anime.objects.order_by("-id")
        serializer = AnimeSerializer(anime, many=True)
        return Response(serializer.data)






