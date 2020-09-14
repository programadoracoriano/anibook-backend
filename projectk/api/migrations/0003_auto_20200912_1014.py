# Generated by Django 3.1.1 on 2020-09-12 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_anime_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=False, null=True, quality=80, size=[800, 600], upload_to='anime'),
        ),
        migrations.CreateModel(
            name='AnimeWatching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episodes_number', models.IntegerField(verbose_name='Number of Episodes')),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.anime', verbose_name='Anime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='AnimeRewatched',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.IntegerField(verbose_name='How many times completed?')),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.anime', verbose_name='Anime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
