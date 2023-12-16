from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from main_app.custom_managers import AuthorManager


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2005)])
    website = models.URLField(blank=True, null=True)

    objects = AuthorManager()


class Article(models.Model):
    class CategoryChoices(models.TextChoices):
        TECHNOLOGY = 'Technology'
        SCIENCE = 'Science'
        EDUCATION = 'Education'

    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(max_length=10, default=CategoryChoices.TECHNOLOGY, choices=CategoryChoices.choices)
    authors = models.ManyToManyField(to=Author, related_name='authors_articles')
    published_on = models.DateTimeField(editable=False, auto_now_add=True)


class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='reviews')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='review_articles')
    published_on = models.DateTimeField(editable=False, auto_now_add=True)
