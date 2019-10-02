# Generated by Django 2.2.4 on 2019-08-19 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='association',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ranking.Association'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ranking.City'),
            preserve_default=False,
        ),
    ]
