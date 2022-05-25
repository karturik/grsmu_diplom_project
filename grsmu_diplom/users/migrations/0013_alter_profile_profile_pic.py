# Generated by Django 4.0.4 on 2022-05-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.CharField(blank=True, choices=[('images/teacher.jpg', 'images/teacher.jpg'), ('images/van.jpg', 'images/van.jpg')], default='images/teacher.jpg', max_length=255),
        ),
    ]
