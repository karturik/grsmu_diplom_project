# Generated by Django 4.0.4 on 2022-05-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0011_teacher_communication_average_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='teacher_pic',
            new_name='teacher_img',
        ),
        migrations.AddField(
            model_name='teacher',
            name='image_src',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
