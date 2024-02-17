from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .managers import UserManager
from django_resized import ResizedImageField #type: ignore
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin): #type: ignore
    email: models.EmailField = models.EmailField(unique=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):
        pass

class Profile(models.Model):
  user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")
  image = ResizedImageField(size=[200, 200], quality=80, keep_meta=False,
                            upload_to='media/profile/', force_format='WEBP',
                            default='profile/user-placeholder.png', null=True)
  cover = ResizedImageField(quality=80, keep_meta=False,
                            upload_to='media/profile/covers/', force_format='WEBP',
                            default='profile/user-placeholder.png', null=True)
  is_moderator: models.BooleanField = models.BooleanField(default=False)

  @property
  def image_url(self):
      return "{0}{1}".format(settings.SITE_URL, self.image.url)

  @property
  def cover_url(self):
      return "{0}{1}".format(settings.SITE_URL, self.cover.url)
