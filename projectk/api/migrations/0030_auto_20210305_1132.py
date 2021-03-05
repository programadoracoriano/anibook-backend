# Generated by Django 3.1.1 on 2021-03-05 11:32

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20210209_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=150, verbose_name='Service')),
                ('icon', django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=False, null=True, quality=80, size=[32, 32], upload_to='services/icon')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='anilist_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Anilist Id'),
        ),
        migrations.AddField(
            model_name='anime',
            name='mal_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='My Anime List Id'),
        ),
        migrations.RemoveField(
            model_name='anime',
            name='stream_source',
        ),
        migrations.AddField(
            model_name='anime',
            name='stream_source',
            field=models.ManyToManyField(blank=True, to='api.StreamSource', verbose_name='Stream Source'),
        ),
        migrations.AddField(
            model_name='streamsource',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.streamservice', verbose_name='Stream Service'),
        ),
    ]
