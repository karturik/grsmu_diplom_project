# Generated by Django 4.0.4 on 2022-05-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0013_alter_teacher_image_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image_src',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
