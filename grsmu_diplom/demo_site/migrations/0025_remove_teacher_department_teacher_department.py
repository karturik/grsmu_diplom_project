# Generated by Django 4.0.4 on 2022-05-14 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0024_alter_comment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='department',
        ),
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ManyToManyField(to='demo_site.department'),
        ),
    ]
