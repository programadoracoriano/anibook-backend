# Generated by Django 3.1.1 on 2020-12-21 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0018_auto_20201123_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=5000, verbose_name='Comment')),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='topic',
            name='categorie',
        ),
        migrations.AddField(
            model_name='topic',
            name='anime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.anime', verbose_name='Anime'),
        ),
        migrations.AlterField(
            model_name='anime',
            name='cover_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=False, null=True, quality=80, size=[800, 600], upload_to='anime_cover'),
        ),
        migrations.DeleteModel(
            name='TopicCategorie',
        ),
        migrations.AddField(
            model_name='topiccomment',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.topic', verbose_name='Topico'),
        ),
        migrations.AddField(
            model_name='topiccomment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]