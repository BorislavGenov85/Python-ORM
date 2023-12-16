import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie


# Create and run your queries within functions

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query |= query_name & query_nationality
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    return '\n'.join(
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}" for d in directors
    )


def get_top_director():
    director = Director.objects.prefetch_related('movies__starring_actor') \
        .annotate(movies_count=Count('movies')).order_by('-movies_count', 'full_name').first()

    if not director:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor():
    actor = Actor.objects.annotate(
        movies_count=Count('starring_actors'),
        avr_ratings=Avg('starring_actors__rating')) .order_by('-movies_count', 'full_name').first()

    if not actor or not actor.movies_count:
        return ''

    movie_titles = ', '.join(m.title for m in actor.starring_actors.all() if m)

    return (f"Top Actor: {actor.full_name}, starring in movies: {movie_titles},"
            f" movies average rating: {actor.avr_ratings:.1f}")

