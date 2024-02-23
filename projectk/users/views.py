from users import models, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication #type: ignore
from rest_framework.permissions import IsAuthenticated


class CreateUserView(APIView):
    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserProfileView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateUserProfileView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        return models.UserProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class RetrieveUserProfileView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        return models.UserProfile.objects.filter(user=self.request.user)
