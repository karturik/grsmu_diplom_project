# Generated by Django 4.0.4 on 2022-06-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='warnings',
            field=models.IntegerField(default=0),
        ),
    ]