import re

from django.core.exceptions import ValidationError


def contains_only_letters_and_spaces_validator(value):
    if not all(character.isalpha() or character.isspace() for character in value):
        raise ValidationError('Name can only contain letters and spaces')

    return value


def age_validator(value):
    if value < 18:
        raise ValidationError('Age must be greater than 18')
    return value


def validate_phone_number(value):
    if not re.match(r'\+359\d{9}', value):
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")

    return value


def validate_author(value):
    if len(value) < 5:
        raise ValidationError("Author must be at least 5 characters long")
    return value


def validate_isbn(value):
    if len(value) < 6:
        raise ValidationError("ISBN must be at least 6 characters long")

    return value


def validate_director(value):
    if len(value) < 8:
        raise ValidationError("Director must be at least 8 characters long")

    return value


def validate_artist(value):
    if len(value) < 9:
        raise ValidationError("Artist must be at least 9 characters long")

    return value