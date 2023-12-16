# Generated by Django 4.2.4 on 2023-11-11 15:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2, 'Name must be at least 2 characters long.'), django.core.validators.MaxLengthValidator(100, 'Name cannot exceed 100 characters.')])),
                ('location', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Location must be at least 2 characters long.'), django.core.validators.MaxLengthValidator(200, 'Location cannot exceed 200 characters.')])),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0, 'Rating must be at least 0.00.'), django.core.validators.MaxValueValidator(5, 'Rating cannot exceed 5.00.')])),
            ],
        ),
    ]