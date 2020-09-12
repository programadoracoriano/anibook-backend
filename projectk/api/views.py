
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LoginAPI(request):            # <-- And here
    if request.method == 'GET':
        user = authenticate(username="peradoce", password="123")
        content = {}
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            print(token)
            u = User.objects.get(auth_token=token)
            content = {'message': u.username}
        return Response(content)

@api_view(['GET'])
def AnimeListAPI(request):
    if request.method == 'GET':
        anime = Anime.objects.order_by("-id")
        serializer = AnimeSerializer(anime, many=True)
        return Response(serializer.data)



