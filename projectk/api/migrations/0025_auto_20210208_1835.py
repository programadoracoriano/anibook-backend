# Generated by Django 3.1.1 on 2021-02-08 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20210208_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animereview',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='animestatus',
            name='date',
            field=models.DateField(),
        ),
    ]
