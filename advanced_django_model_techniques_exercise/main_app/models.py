from decimal import Decimal

from django.db import models

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import (contains_only_letters_and_spaces_validator, age_validator,
                                 validate_phone_number, validate_author, validate_isbn,
                                 validate_director, validate_artist)


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100, validators=[contains_only_letters_and_spaces_validator])
    age = models.PositiveIntegerField(validators=[age_validator])
    email = models.EmailField(error_messages={'invalid': 'Enter a valid email address'})
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    website_url = models.URLField(error_messages={'invalid': "Enter a valid URL"})


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'title']
        abstract = True


class Book(BaseMedia):
    author = models.CharField(max_length=100, validators=[validate_author])
    isbn = models.CharField(max_length=20, validators=[validate_isbn])

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Movie(BaseMedia):
    director = models.CharField(max_length=100, validators=[validate_director])

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = 'Models of type - Movie'


class Music(BaseMedia):
    artist = models.CharField(max_length=100, validators=[validate_artist])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = "Models of type - Music"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return self.price * Decimal(0.08)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(2)

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):

    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        return self.price * Decimal(1.2)

    def calculate_tax(self):
        return self.price * Decimal(0.05)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(1.50)

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()


class SpiderHero(Hero):
    class Meta:
        proxy = True

    def swing_from_buildings(self):
        current_energy = self.energy - 80

        if current_energy <= 0:
            return f"{self.name} as Spider Hero is out of web shooter fluid"

        self.energy = current_energy
        self.save()

        return f"{self.name} as Spider Hero swings from buildings using web shooters"


class FlashHero(Hero):
    class Meta:
        proxy = True

    def run_at_super_speed(self):
        current_energy = self.energy - 65

        if current_energy <= 0:
            return f"{self.name} as Flash Hero needs to recharge the speed force"

        self.energy = current_energy
        self.save()

        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"
