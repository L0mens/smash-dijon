# Generated by Django 2.2.4 on 2020-09-27 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0040_siteoptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='slug',
            field=models.CharField(max_length=255),
        ),
    ]
