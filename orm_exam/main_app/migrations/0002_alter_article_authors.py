# Generated by Django 4.2.4 on 2023-11-27 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(related_name='authors_articles', to='main_app.author'),
        ),
    ]
