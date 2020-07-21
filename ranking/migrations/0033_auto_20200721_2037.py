# Generated by Django 2.2.4 on 2020-07-21 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0032_saison_eligibilty_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='saison',
            name='previous_saison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ranking.Saison'),
        ),
        migrations.AddField(
            model_name='saison',
            name='split_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
