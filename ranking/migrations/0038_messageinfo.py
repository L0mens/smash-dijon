# Generated by Django 2.2.4 on 2020-08-03 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0037_saison_hidden'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=255)),
                ('status', models.CharField(choices=[('active', 'active'), ('archive', 'archive')], max_length=255)),
                ('message_type', models.CharField(choices=[('info', 'Information'), ('warning', 'Attention'), ('error', 'Erreur')], max_length=255)),
            ],
        ),
    ]
