# Generated by Django 4.0.4 on 2022-05-16 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0034_remove_likebutton_content_likebutton_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likebutton',
            old_name='likes',
            new_name='user',
        ),
    ]
