# Generated by Django 4.0.4 on 2022-05-06 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_site', '0008_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='communication',
            field=models.IntegerField(default=0, verbose_name='Коммуникация'),
        ),
    ]
