# Generated by Django 2.2.4 on 2020-03-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0028_auto_20200304_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='elo',
            name='is_away',
            field=models.BooleanField(default=False, verbose_name='Ne participe plus'),
        ),
    ]
