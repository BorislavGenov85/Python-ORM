# Generated by Django 4.2.4 on 2023-12-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(related_name='match_players', to='main_app.tennisplayer'),
        ),
    ]
