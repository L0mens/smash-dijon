# Generated by Django 2.2.4 on 2019-10-27 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0018_auto_20191023_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]