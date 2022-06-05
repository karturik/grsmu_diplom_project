# Generated by Django 4.0.4 on 2022-05-30 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0044_comment_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='category',
            field=models.CharField(choices=[('lesson', 'Занятия'), ('lection', 'Лекции'), ('exam', 'Экзамены'), ('other', 'Остальное')], default='other', max_length=10),
        ),
    ]