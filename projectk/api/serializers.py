from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('id', 'categorie',)

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ('id', 'name', 'founded')

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ('id', 'name', 'episodes_number', 'minutes_per_episode', 'sinopse', 'studio_name', 'categorie_categorie')

    studio_name         = serializers.SerializerMethodField('get_studio_name')
    categorie_categorie = serializers.SerializerMethodField('get_categorie_categorie')

    def get_studio_name(self, obj):
        return obj.studio.name

    def get_categorie_categorie(self, obj):
        return obj.categorie.categorie
