# Generated by Django 2.2.4 on 2020-01-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0025_city_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='elo',
            name='main_char_skin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='elo',
            name='second_char_skin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='elo',
            name='third_char_skin',
            field=models.IntegerField(default=0),
        ),
    ]
