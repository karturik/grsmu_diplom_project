# Generated by Django 4.0.4 on 2022-05-15 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demo_site', '0029_alter_teacher_communication_average_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentanswer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
