# Generated by Django 4.2.4 on 2023-11-11 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_menureview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodcriticrestaurantreview',
            options={'verbose_name': 'Food Critic Review', 'verbose_name_plural': 'Food Critic Reviews'},
        ),
        migrations.AlterModelOptions(
            name='regularrestaurantreview',
            options={'verbose_name': 'Restaurant Review', 'verbose_name_plural': 'Restaurant Reviews'},
        ),
    ]
