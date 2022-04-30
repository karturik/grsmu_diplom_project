# Generated by Django 4.0.4 on 2022-04-30 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='course',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='media/user.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
