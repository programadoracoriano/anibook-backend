# Generated by Django 3.1.1 on 2021-02-08 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20210208_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animestatus',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
