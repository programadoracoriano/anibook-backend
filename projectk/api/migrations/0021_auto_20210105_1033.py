# Generated by Django 3.1.1 on 2021-01-05 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20210104_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.IntegerField(verbose_name='Season Number')),
                ('tag', models.CharField(max_length=100, verbose_name='Designation')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='season_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.seasonnumber', verbose_name='Season'),
        ),
    ]
