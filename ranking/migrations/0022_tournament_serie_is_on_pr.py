# Generated by Django 2.2.4 on 2019-10-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0021_auto_20191030_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament_serie',
            name='is_on_pr',
            field=models.BooleanField(default=True),
        ),
    ]