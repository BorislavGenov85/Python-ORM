import os
import django
from django.db.models import Count, Q, Sum, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


# Create and run your queries within functions

def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query |= query_name & query_email
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ''

    result = []
    for author in authors:
        banned = ''
        if author.is_banned:
            banned = 'Banned'
        else:
            banned = 'Not Banned'
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {banned}")

    return '\n'.join(result)


def get_top_publisher():
    if not Article.objects.exists():
        return ''

    author = Author.objects.annotate(
        articles_count=Count('articles_authors')
    ).order_by('-articles_count', 'email').first()

    return f"Top Author: {author.full_name} with {author.articles_count} published articles."


def get_top_reviewer():
    if not Review.objects.exists():
        return ''

    author = Author.objects.annotate(
        reviews_count=Count('reviews')
    ).order_by('-reviews_count', 'email').first()

    return f"Top Reviewer: {author.full_name} with {author.reviews_count} published reviews."


def get_latest_article():
    if not Article.objects.exists():
        return ''

    article = Article.objects.prefetch_related(
        'authors__reviews'
    ).annotate(review_count=Count('articles'),
               total_rating=Sum('articles__rating')
               ).order_by('-published_on').first()

    if not article:
        return ''

    authors_name = ', '.join([a.full_name for a in article.authors.all().order_by('full_name')])
    avg_rating = article.total_rating / article.review_count if article.review_count else 0

    return (f"The latest article is: {article.title}. Authors: {authors_name}. "
            f"Reviewed: {article.review_count} times. Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    article = Article.objects.annotate(
        avg_rating=Avg('articles__rating')
    ).exclude(avg_rating=None).order_by('-avg_rating', 'title').first()

    review_count = article.articles.count() if article else 0
    if article is None or review_count == 0:
        return ""

    return (f"The top-rated article is: {article.title}, with an average rating of {article.avg_rating:.2f},"
            f" reviewed {review_count} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    if not Author.objects.exists():
        return "No authors banned."

    author = Author.objects.prefetch_related(
        'reviews'
    ).annotate(
        review_count=Count('reviews')
    ).filter(email__exact=email).first()

    if not author:
        return "No authors banned."

    author.is_banned = True
    author.save()

    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {author.review_count} reviews deleted."
