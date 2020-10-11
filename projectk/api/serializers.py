from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.serializers import ReadOnlyField


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'image')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, many=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'profile')

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('id', 'categorie',)

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ('id', 'name', 'founded')

class LicensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licensor
        fields = ('id', 'name')

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('id', 'name')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'rating',)

class AnimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = AnimeType
        fields  = ('id', 'type',)

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Source
        fields  = ('id', 'source',)

class AnimeSerializer(serializers.ModelSerializer):
    categorie   = CategorieSerializer(read_only=True, many=True)
    studio      = StudioSerializer(read_only=True, many=True)
    rating      = RatingSerializer(read_only=True)
    type        = AnimeTypeSerializer(read_only=True)
    source      = SourceSerializer(read_only=True)
    licensors    = LicensorSerializer(read_only=True, many=True)
    producers    = ProducerSerializer(read_only=True, many=True)
    class Meta:
        model   = Anime
        fields  = ('id', 'name', 'episodes_number', 'minutes_per_episode', 'aired','sinopse', 'image', 'studio', 'categorie',
                  'rating', 'type', 'source', 'licensors', 'producers',)

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Status
        fields  = ('id', 'val', 'tag',)


class AnimeStatusSerializer(serializers.ModelSerializer):
    anime   = AnimeSerializer(read_only=True, many=False)
    user    = UserSerializer(read_only=True, many=False)
    status  = StatusSerializer(read_only=True, many=False)
    class Meta:
        model   = AnimeStatus
        fields  = ('anime' , 'user', 'episodes_number', 'completed', 'status', 'score')

class FollowerSerializer(serializers.ModelSerializer):
    user    = UserSerializer(read_only=True, many=False)
    class Meta:
        model   = Followers
        fields  = ('follower' , 'followers')

class CustomListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    anime = AnimeSerializer(read_only=True, many=False)
    class Meta:
        model   = CustomList
        fields  = ('user' , 'title', 'main_anime')








