# Generated by Django 4.0.4 on 2022-04-16 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0002_rename_post_comment_teacher_alter_department_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=30),
        ),
    ]
