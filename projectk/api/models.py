from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# Create your models here.



class Categorie(models.Model):
    categorie = models.CharField(max_length=75, null=False, blank=False, verbose_name="Categorie")
    def __str__(self):
        return self.categorie

class Studio(models.Model):
    name    = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    founded = models.DateField(null=False, blank=False, verbose_name="Year of Foundation")
    def __str__(self):
        return self.name

class Anime(models.Model):
    name                = models.CharField(max_length=300, null=False, blank=False, verbose_name="Anime Name")
    episodes_number     = models.IntegerField(null=False, blank=False, verbose_name="Number of Episodes")
    minutes_per_episode = models.IntegerField(null=False, blank=False, verbose_name="Minutes per Episode")
    sinopse             = models.TextField(max_length=800, blank=False, null=False, verbose_name="Sinopse")
    studio              = models.ForeignKey(Studio, null=False, blank=False, verbose_name="Studio", on_delete=models.CASCADE)
    categorie           = models.ForeignKey(Categorie, null=True, blank=False, verbose_name="Categorie", on_delete=models.CASCADE)
    def __str__(self):
        return self.name



