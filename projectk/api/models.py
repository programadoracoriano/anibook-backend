from django.db import models #type: ignore
from django.contrib.auth.models import User #type: ignore
from django_resized import ResizedImageField #type: ignore
from django.db.models.signals import post_save #type: ignore
from django.dispatch import receiver #type: ignore
# Create your models here.
from django.conf import settings #type: ignore


class Categorie(models.Model):
    categorie = models.CharField(max_length=75, null=False, blank=False, verbose_name="Categorie")
    categorie_pt = models.CharField(max_length=75, null=True, blank=True, verbose_name="Categorie(Portuguese)")
    def __str__(self):
        return self.categorie

class Rating(models.Model):
    rating = models.CharField(max_length=150, null=False, blank=False, verbose_name="Rating")

    def __str__(self):
        return self.rating

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = ResizedImageField(size=[200, 200], quality=80, keep_meta=False,
                            upload_to='media/profile/', force_format='JPEG',
                            default='profile/user-placeholder.png', null=True)
  cover = ResizedImageField(quality=80, keep_meta=False,
                            upload_to='media/profile/covers/', force_format='JPEG',
                            default='profile/user-placeholder.png', null=True)
  points = models.IntegerField(null=True, blank=True, default=0)
  blockuser = models.ManyToManyField(User, related_name="blockuser")
  rating = models.ManyToManyField(Rating)

  @property
  def image_url(self):
      return "{0}{1}".format(settings.SITE_URL, self.image.url)

  @property
  def cover_url(self):
      return "{0}{1}".format(settings.SITE_URL, self.cover.url)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class DefaultAvatar(models.Model):
    tag = models.CharField(max_length=75, null=False, blank=False, verbose_name="Characters")
    image = ResizedImageField(size=[200, 200], quality=80, keep_meta=False,
                        upload_to='avatar', force_format='JPEG',
                        default='profile/user-placeholder.png', null=True)
    def __str__(self):
        return self.tag

    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

class UserContentStatus(models.Model):
    val = models.IntegerField(null=False, blank=False, verbose_name="Numéric Value")
    status = models.CharField(max_length=75, null=False, blank=False, verbose_name="Status")

    def __str__(self):
        return self.status

class AnimeType(models.Model):
    tpe = models.CharField(max_length=75, null=False, blank=False, verbose_name="Type")
    type_pt = models.CharField(max_length=75, null=True, blank=True, verbose_name="Type(Portuguese)")
    def __str__(self):
        return self.type

class AlternativeTitle(models.Model):
    title = models.CharField(max_length=75, null=False, blank=False, verbose_name="Title")
    def __str__(self):
        return self.title

class Studio(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    founded = models.DateField(null=True, blank=True, verbose_name="Year of Foundation")
    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    def __str__(self):
        return self.name

class Licensor(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Studio Name")
    def __str__(self):
        return self.name

class Source(models.Model):
    source = models.CharField(max_length=150, null=False, blank=False, verbose_name="Source")
    def __str__(self):
        return self.source

class DateOption(models.Model):
    tag = models.CharField(max_length=150, null=False, blank=False, verbose_name="Date Option")
    def __str__(self):
        return self.tag

class StreamService(models.Model):
    service = models.CharField(max_length=150, null=False, blank=False, verbose_name="Service")
    icon = ResizedImageField(null=True, blank=False, size=[32, 32], keep_meta=False, quality=80, upload_to='services/icon',
                              force_format='PNG')
    def __str__(self):
        return self.service

class StreamSource(models.Model):
    service = models.ForeignKey(StreamService, null=True, blank=False, verbose_name="Stream Service", on_delete=models.CASCADE)
    source = models.CharField(max_length=150, null=False, blank=False, verbose_name="Source")
    def __str__(self):
        return self.source

class SeasonNumber(models.Model):
    val = models.IntegerField(null=False, blank=False, verbose_name="Season Number")
    tag = models.CharField(null=False, blank=False, max_length=100, verbose_name="Designation")
    def __str__(self):
        return self.tag

class Anime(models.Model):
    cover_image =  ResizedImageField(null=True, blank=True, keep_meta=False, quality=80, upload_to='quizz',
                              force_format='JPEG')
    image = ResizedImageField(null=True, blank=True, keep_meta=False, quality=80, upload_to='quizz',
                              force_format='JPEG')
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name="Anime Name")
    alternative_title = models.ManyToManyField(AlternativeTitle, blank=True, verbose_name="Alternative Title")
    season_number = models.ForeignKey(SeasonNumber, null=True, blank=True, verbose_name="Season", on_delete=models.CASCADE)
    tpe = models.ForeignKey(AnimeType, null=True, blank=True, verbose_name="Type", on_delete=models.CASCADE)
    episodes_number = models.IntegerField(null=True, blank=True, verbose_name="Number of Episodes")
    minutes_per_episode = models.IntegerField(null=True, blank=True, verbose_name="Minutes per Episode")
    date_option = models.ForeignKey(DateOption, null=True, blank=True, verbose_name="Date Option(Aired)", on_delete=models.CASCADE)
    aired = models.DateField(verbose_name="Aired", null=True, blank=True)
    date_end = models.DateField(verbose_name="End Date", null=True, blank=True)
    producers = models.ManyToManyField(Producer, blank=True, verbose_name="Producers")
    licensors  = models.ManyToManyField(Licensor, blank=True, verbose_name="Licensors")
    studio = models.ManyToManyField(Studio, blank=True, verbose_name="Studio")
    source = models.ForeignKey(Source, null=True, blank=True, verbose_name="Source", on_delete=models.CASCADE)
    categorie = models.ManyToManyField(Categorie, blank=True, verbose_name="Genre")
    rating = models.ForeignKey(Rating, null=True, blank=True,  verbose_name="Rating", on_delete=models.CASCADE)
    sinopse =  models.TextField(max_length=1500, blank=True, null=True, verbose_name="Synopsis")
    sinopse_pt = models.TextField(max_length=1500, blank=True, null=True, verbose_name="Synopsis(Portuguese)")
    trailer = models.CharField(max_length=100, blank=True, null=True, verbose_name="Trailer(Youtube ID)")
    stream_source = models.ManyToManyField(StreamSource, blank=True,  verbose_name="Stream Source")
    mal_id  = models.IntegerField(null=True, blank=True, verbose_name="My Anime List Id")
    anilist_id = models.IntegerField(null=True, blank=True, verbose_name="Anilist Id")
    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    @property
    def cover_image_url(self):
        if self.cover_image:
            return "{0}{1}".format(settings.SITE_URL, self.cover_image.url)

    def __str__(self):
        return self.name

class Topic(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="User", on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, null=True, blank=True, verbose_name="Anime", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name="title")
    description = models.TextField(max_length=5000, null=False, blank=False, verbose_name="Description")
    image = ResizedImageField(null=True, blank=True, size=[800, 600], keep_meta=False, quality=80, upload_to='topicimages',
                              force_format='JPEG')
    date = models.DateField(auto_now=True)

class TopicComment(models.Model):
    topic = models.ForeignKey(Topic, null=True, blank=True, verbose_name="Topico", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="User", on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000, null=False, blank=False, verbose_name="Comment")
    date = models.DateField(auto_now=True)


class Status(models.Model):
    val = models.IntegerField(null=False, blank=False, verbose_name="Value")
    tag = models.CharField(max_length=100, null=False, blank=False, verbose_name="Tag")
    tag_pt = models.CharField(max_length=100, null=True, blank=False, verbose_name="Tag(Portuguese)")
    def __str__(self):
        return self.tag

class AnimeStatus(models.Model):
    anime = models.ForeignKey(Anime, null=False, blank=False, verbose_name="Anime", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, verbose_name="User", on_delete=models.CASCADE)
    episodes_number = models.IntegerField(null=True, blank=True, verbose_name="Number of Episodes")
    completed = models.IntegerField(null=True, blank=True, verbose_name="How many times completed?")
    status = models.ForeignKey(Status, null=True, blank=True, verbose_name="Status", on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True, verbose_name="Score")
    note = models.TextField(max_length=500, null=True, blank=True, verbose_name="Notes")
    date = models.DateTimeField()

class AnimeReview(models.Model):
    anime = models.ForeignKey(Anime, null=True, blank=True, verbose_name="Anime", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="User", on_delete=models.CASCADE)
    review = models.TextField(max_length=5000, null=False, blank=False, verbose_name="Review")
    draft = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(AnimeStatus, null=True, blank=True, verbose_name="Status", on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

class Followers(models.Model):
    follower = models.ForeignKey(User, null=False, blank=False, verbose_name="Anime", on_delete=models.CASCADE)
    followers = models.IntegerField(null=False, blank=True)

class CustomList(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, verbose_name="User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Title")
    image = ResizedImageField(null=True, blank=False, keep_meta=False, quality=80, upload_to='custom_list',
                      force_format='JPEG')

    @property
    def image_url(self):
        if self.image:
            return "{0}{1}".format(settings.SITE_URL, self.image.url)

class AnimeCustomList(models.Model):
    custom_list = models.ForeignKey(CustomList, null=True, blank=False, verbose_name="CustomList", on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, null=True, blank=False, verbose_name="Anime", on_delete=models.CASCADE)

class CollectPoint(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, verbose_name="User", on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

class ReportMotive(models.Model):
    motive = models.CharField(max_length=100, blank=False, null=False, verbose_name="Motive")
    def __str__(self):
        return self.motive

class ReportSection(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, verbose_name="User", on_delete=models.CASCADE)
    tpe = models.CharField(max_length=100, blank=False, null=False, verbose_name="Type")
    pid = models.CharField(max_length=100, blank=False, null=False, verbose_name="ID")
    motive = models.ForeignKey(ReportMotive, null=False, blank=False, verbose_name="Motive", on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

class QuizzLevel(models.Model):
    val = models.IntegerField(null=False, blank=False, verbose_name="Valor do Nível")
    level = models.CharField(max_length=100, blank=False, null=False, verbose_name="Level")

class Quizz(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, verbose_name="User", on_delete=models.CASCADE)
    question = models.CharField(max_length=360, blank=False, null=False, verbose_name="Question")
    image = ResizedImageField(null=True, blank=True, keep_meta=False, quality=80, upload_to='quizz',
                              force_format='JPEG')
    level = models.ForeignKey(QuizzLevel, null=False, blank=False, verbose_name="Level", on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, null=False, blank=False, verbose_name="Anime", on_delete=models.CASCADE)
    status = models.ForeignKey(UserContentStatus, null=False, blank=False, verbose_name="Status", on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)
