from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, ImageField

from .models import *
from django.contrib.auth.models import User
from rest_framework.serializers import ReadOnlyField


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'image_url', 'cover_url', 'points',)

class DefaultAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAvatar
        fields = ('id', 'tag', 'image_url')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, many=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'profile', 'email')

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

class StreamSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = StreamSource
        fields  = ('id', 'source',)

class SeasonNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model   = SeasonNumber
        fields  = ('id', 'val', 'tag')

class DateOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model   = DateOption
        fields  = ('id', 'tag')


class AnimeSerializer(serializers.ModelSerializer):
    categorie       = CategorieSerializer(read_only=True, many=True)
    studio          = StudioSerializer(read_only=True, many=True)
    rating          = RatingSerializer(read_only=True)
    type            = AnimeTypeSerializer(read_only=True)
    source          = SourceSerializer(read_only=True)
    licensors       = LicensorSerializer(read_only=True, many=True)
    producers       = ProducerSerializer(read_only=True, many=True)
    season_number   = SeasonNumberSerializer(read_only=True, many=False)
    date_option     = DateOptionSerializer(read_only=True, many=False)
    class Meta:
        model   = Anime
        fields  = ('id', 'name', 'season_number','episodes_number', 'minutes_per_episode', 'date_option', 'aired', 'date_end', 'sinopse', 'image_url', 'cover_image_url'
                   ,'studio', 'categorie', 'rating', 'type', 'source', 'licensors', 'producers', 'trailer')



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
        fields  = ('id', 'anime' , 'user', 'episodes_number', 'completed', 'status', 'score', 'note',)

class FollowerSerializer(serializers.ModelSerializer):
    follower    = UserSerializer(read_only=True, many=False)
    class Meta:
        model   = Followers
        fields  = ('follower' , 'followers')

class CustomListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    class Meta:
        model   = CustomList
        fields  = ('id', 'user' , 'title', 'image_url')

class AnimeCustomListSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer(read_only=True, many=False)
    class Meta:
        model   = AnimeCustomList
        fields  = ('id' , 'anime')


class AnimeReviewSerializer(serializers.ModelSerializer):
    anime   = AnimeSerializer(read_only=True, many=False)
    user    = UserSerializer(read_only=True, many=False)
    status  = AnimeStatusSerializer(read_only=True, many=False)
    class Meta:
        model   = AnimeReview
        fields  = ('id', 'anime', 'user', 'review', 'draft', 'status', 'date')


class TopicSerializer(serializers.ModelSerializer):
    user        = UserSerializer(read_only=True, many=False)
    anime       = AnimeSerializer(read_only=True, many=False)
    class Meta:
        model   = Topic
        fields  = ('id' , 'user', 'categorie', 'title', 'description', 'date')










