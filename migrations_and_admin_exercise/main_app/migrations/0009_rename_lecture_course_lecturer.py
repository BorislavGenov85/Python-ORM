# Generated by Django 4.2.4 on 2023-10-26 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='lecture',
            new_name='lecturer',
        ),
    ]
