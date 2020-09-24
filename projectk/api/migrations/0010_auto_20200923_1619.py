# Generated by Django 3.1.1 on 2020-09-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200918_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animestatus',
            name='completed',
            field=models.IntegerField(blank=True, null=True, verbose_name='How many times completed?'),
        ),
        migrations.AlterField(
            model_name='animestatus',
            name='episodes_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of Episodes'),
        ),
    ]
