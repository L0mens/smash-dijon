# Generated by Django 2.2.4 on 2019-10-30 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0019_auto_20191027_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament_serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo_url', models.URLField(default='', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='city',
        ),
        migrations.CreateModel(
            name='Tournament_place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo_url', models.URLField(default='', null=True)),
                ('adress', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.City')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ranking.Tournament_place'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='serie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ranking.Tournament_serie'),
        ),
    ]
