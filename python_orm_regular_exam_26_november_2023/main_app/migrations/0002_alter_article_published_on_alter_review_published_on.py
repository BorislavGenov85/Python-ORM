# Generated by Django 4.2.4 on 2023-12-03 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='published_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
