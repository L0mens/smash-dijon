# Generated by Django 2.2.4 on 2020-07-21 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0034_auto_20200721_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saison',
            name='split_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
