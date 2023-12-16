import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create and run your queries within functions

def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query |= query_name & query_country
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_country

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players:
        return ''

    result = [f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}" for p in players]

    return '\n'.join(result)


def get_top_tennis_player():
    if not TennisPlayer.objects.exists():
        return ''

    player = TennisPlayer.objects.annotate(
        win_count=Count('match_winner')
    ).order_by('-win_count', 'full_name').first()

    if not player:
        return ''

    return f"Top Tennis Player: {player.full_name} with {player.win_count} wins."


def get_tennis_player_by_matches_count():
    if not TennisPlayer.objects.exists() or not Match.objects.exists():
        return ''

    player = TennisPlayer.objects.annotate(
        match_count=Count('match_players')
    ).order_by('-match_count', 'ranking').first()

    if not player:
        return ''

    return f"Tennis Player: {player.full_name} with {player.match_count} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    if not Tournament.objects.exists():
        return ''

    tournaments = Tournament.objects.annotate(
        num_matches=Count('matches')
    ).filter(surface_type__icontains=surface).order_by('-start_date')

    if not tournaments:
        return ''

    result = [f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}" for t in tournaments]

    return '\n'.join(result)


def get_latest_match_info():
    if not Match.objects.exists():
        return ''

    match = Match.objects.prefetch_related(
        'winner__match_players__tournament'
    ).order_by('date_played', 'id').last()

    if not match:
        return ''

    tournament_name = match.tournament.name
    players_names = [p.full_name for p in match.players.all().order_by('full_name')]
    winner = match.winner.full_name if match.winner is not None else "TBA"

    return (f"Latest match played on: {match.date_played}, tournament: {tournament_name},"
            f" score: {match.score}, players: {' vs '.join(players_names)},"
            f" winner: {winner}, summary: {match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    if not Tournament.objects.exists():
        return "No matches found."

    matches = Match.objects.prefetch_related(
        'tournament'
    ).filter(tournament__name__exact=tournament_name).order_by('-date_played')

    if not matches:
        return "No matches found."

    result = []

    for m in matches:
        result.append(f'Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else "TBA"}')

    return '\n'.join(result)


