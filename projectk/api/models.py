from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
  user        = models.OneToOneField(User, on_delete=models.CASCADE)
  image       = ResizedImageField(size=[200, 200], quality=80, keep_meta=False,
                            upload_to='media/profile/', force_format='JPEG',
  default='profile/user-placeholder.png', null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Categorie(models.Model):
    categorie = models.CharField(max_length=75, null=False, blank=False, verbose_name="Categorie")
    def __str__(self):
        return self.categorie

class AnimeType(models.Model):
    type = models.CharField(max_length=75, null=False, blank=False, verbose_name="Type")
    def __str__(self):
        return self.type

class AlternativeTitle(models.Model):
    title = models.CharField(max_length=75, null=False, blank=False, verbose_name="Title")
    def __str__(self):
        return self.title

class Studio(models.Model):
    name    = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    founded = models.DateField(null=True, blank=True, verbose_name="Year of Foundation")
    def __str__(self):
        return self.name

class Producer(models.Model):
    name    = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    def __str__(self):
        return self.name

class Licensor(models.Model):
    name    = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    def __str__(self):
        return self.name

class Source(models.Model):
    source    = models.CharField(max_length=150, null=False, blank=False, verbose_name="Source")
    def __str__(self):
        return self.source

class Rating(models.Model):
    rating = models.CharField(max_length=150, null=False, blank=False, verbose_name="Rating")

    def __str__(self):
        return self.rating

class Anime(models.Model):
    image               = ResizedImageField(null=True, blank=False, size=[800, 600], keep_meta=False, quality=80, upload_to='anime',
                              force_format='JPEG')
    name                =   models.CharField(max_length=300, null=False, blank=False, verbose_name="Anime Name")
    alternative_title   =   models.ManyToManyField(AlternativeTitle, blank=True, verbose_name="Alternative Title")
    type                =   models.ForeignKey(AnimeType, null=True, blank=True, verbose_name="Type", on_delete=models.CASCADE)
    episodes_number     =   models.IntegerField(null=True, blank=True, verbose_name="Number of Episodes")
    minutes_per_episode =   models.IntegerField(null=True, blank=True, verbose_name="Minutes per Episode")
    aired               =   models.DateField(verbose_name="Aired", null=True, blank=True)
    date_end            =   models.DateField(verbose_name="End Date", null=True, blank=True)
    producers           =   models.ManyToManyField(Producer, blank=True, verbose_name="Producers")
    licensors           =   models.ManyToManyField(Licensor, blank=True, verbose_name="Licensors")
    studio              =   models.ManyToManyField(Studio, blank=True, verbose_name="Studio")
    source              =   models.ForeignKey(Source, null=True, blank=True, verbose_name="Source", on_delete=models.CASCADE)
    categorie           =   models.ManyToManyField(Categorie, blank=True, verbose_name="Genre")
    rating              =   models.ForeignKey(Rating, null=True, blank=True,  verbose_name="Rating", on_delete=models.CASCADE)
    sinopse             =   models.TextField(max_length=800, blank=True, null=False, verbose_name="Synopsis")

    def __str__(self):
        return self.name

class Status(models.Model):
    val = models.IntegerField(null=False, blank=False, verbose_name="Value")
    tag = models.CharField(max_length=100, null=False, blank=False, verbose_name="Tag")
    def __str__(self):
        return self.tag

class AnimeStatus(models.Model):
    anime           = models.ForeignKey(Anime, null=False, blank=False, verbose_name="Anime", on_delete=models.CASCADE)
    user            = models.ForeignKey(User, null=False, blank=False, verbose_name="User", on_delete=models.CASCADE)
    episodes_number = models.IntegerField(null=True, blank=True, verbose_name="Number of Episodes")
    completed       = models.IntegerField(null=True, blank=True, verbose_name="How many times completed?")
    status          = models.ForeignKey(Status, null=False, blank=False, verbose_name="Status", on_delete=models.CASCADE)
    score           = models.IntegerField(null=True, blank=False, verbose_name="Score")
    note            = models.TextField(max_length=500, null=True, blank=True, verbose_name="Notes")

class Followers(models.Model):
    follower    = models.ForeignKey(User, null=False, blank=False, verbose_name="Anime", on_delete=models.CASCADE)
    followers   = models.IntegerField(null=False, blank=True)

class CustomList(models.Model):
    user        = models.ForeignKey(User, null=True, blank=False, verbose_name="User", on_delete=models.CASCADE)
    title       = models.CharField(max_length=100, null=False, blank=False, verbose_name="Title")
    image       = ResizedImageField(null=True, blank=False, size=[800, 600], keep_meta=False, quality=80, upload_to='custom_list',
                      force_format='JPEG')

class AnimeCustomList(models.Model):
    custom_list = models.ForeignKey(CustomList, null=True, blank=False, verbose_name="CustomList", on_delete=models.CASCADE)
    anime       = models.ForeignKey(Anime, null=True, blank=False, verbose_name="Anime", on_delete=models.CASCADE)









