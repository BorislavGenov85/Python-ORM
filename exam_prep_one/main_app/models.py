from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models

from main_app.mixins import PersonMixin, AwardedMixin, TimestampMixin
from main_app.custom_managers import DirectorManager


# Create your models here.
class Director(PersonMixin):
    years_of_experience = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(PersonMixin, AwardedMixin, TimestampMixin):
    ...


class Movie(AwardedMixin, TimestampMixin):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action'
        COMEDY = 'Comedy'
        DRAMA = 'Drama'
        OTHER = 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5), MaxLengthValidator(150)]
    )
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0
    )
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='starring_actors'
    )
    actors = models.ManyToManyField(to=Actor)
