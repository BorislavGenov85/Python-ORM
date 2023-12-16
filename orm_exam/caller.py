import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review
from django.db.models import Q, Count, Sum, Avg


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
        status = ''

        if author.is_banned:
            status = 'Banned'
        else:
            status = 'Not Banned'

        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return '\n'.join(result)


def get_top_publisher():
    author = Author.objects.annotate(
        article_count=Count('authors_articles')
    ).filter(article_count__gt=0).order_by('-article_count', 'email').first()

    if not author:
        return ''

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(
        reviews_count=Count('reviews')
    ).filter(reviews_count__gt=0).order_by('-reviews_count', 'email').first()

    if not author:
        return ''

    return f"Top Reviewer: {author.full_name} with {author.reviews_count} published reviews."


def get_latest_article():
    article = Article.objects.annotate(
        review_count=Count('review_articles'),
        sum_ratings=Sum('review_articles__rating')).last()

    if not article:
        return ''

    avg_rating = 0
    if article.review_count == 0:
        avg_rating = 0
    else:
        avg_rating = article.sum_ratings / article.review_count

    names = ', '.join(a.full_name for a in article.authors.order_by('full_name'))

    return (f"The latest article is: {article.title}. Authors: {names}. "
            f"Reviewed: {article.review_count} times. Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    if not Review.objects.all():
        return ''

    article = Article.objects.annotate(
        review_count=Count('review_articles'),
        avg_rating=Avg('review_articles__rating')
    ).order_by('title').first()

    if not article or not article.review_articles.all():
        return ''

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.avg_rating:.2f}, reviewed {article.review_count} times.")


def ban_author(email=None):
    if not Author.objects.all() or email is None:
        return "No authors banned."

    author = Author.objects.prefetch_related('reviews').annotate(
        reviews_count=Count('reviews')
    ).filter(email__exact=email).first()

    if not author:
        return "No authors banned."

    for review in author.reviews.all():
        Review.objects.get(id=review.id).delete()

    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {author.reviews_count} reviews deleted."

# author1 = Author.objects.create(
#     full_name="First Author",
#     email="first@hotmail.com",
#     is_banned=False,
#     birth_year=1999
# )
#
# author2 = Author.objects.create(
#     full_name="Second Author",
#     email="second@hotmail.com",
#     is_banned=False,
#     birth_year=1995
# )
#
# article1 = Article.objects.create(
#     title="First Article",
#     content='idkkkkkkkkkkkkkkkkkkkkkkkkk',
#     category='Science'
# )
#
# article1.authors.add(author1)
#
# article2 = Article.objects.create(
#     title="Second Article",
#     content='idkkkkkkkkkkk222222222222222222',
# )
#
# article2.authors.add(author1, author2)
#
# review1 = Review.objects.create(
#     content='firstttttttttttttttttttttttt',
#     rating=4.9,
#     author=author1,
#     article=article1
# )
#
# review2 = Review.objects.create(
#     content='seconddddddddddddddddddddddddd',
#     rating=3.1,
#     author=author2,
#     article=article2
# )
