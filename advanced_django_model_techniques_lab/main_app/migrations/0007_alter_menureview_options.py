# Generated by Django 4.2.4 on 2023-11-11 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_foodcriticrestaurantreview_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menureview',
            options={'verbose_name': 'Menu Review', 'verbose_name_plural': 'Menu Reviews'},
        ),
    ]
