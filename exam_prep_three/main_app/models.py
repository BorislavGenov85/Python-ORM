from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

from main_app.custom_manager import DirectorManager


# Create your models here.
class Person(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')


class IsAwarded(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(default=False)


class TimestampModel(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(auto_now=True)


class Director(Person):
    years_of_experience = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(Person, IsAwarded, TimestampModel):
    ...


class Movie(IsAwarded, TimestampModel):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action'
        COMEDY = 'Comedy'
        DRAMA = 'Drama'
        OTHER = 'Other'

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=6, default=GenreChoices.OTHER, choices=GenreChoices.choices)
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey(
        to=Actor, on_delete=models.SET_NULL, blank=True, null=True, related_name='starring_actors'
    )
    actors = models.ManyToManyField(to=Actor)
