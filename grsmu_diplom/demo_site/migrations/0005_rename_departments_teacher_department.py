# Generated by Django 4.0.4 on 2022-05-04 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0004_teacher_teacher_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='departments',
            new_name='department',
        ),
    ]
