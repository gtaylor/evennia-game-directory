from collections import Counter

from evennia_gamedir import models, app
from evennia_gamedir.metrics.metric_defines import EvenniaPlayerConnected, \
    EvenniaPlayersAll, EDGGameListingsAll, EDGGameListingsFresh


@app.route('/_cron/metrics/frequent-all-game-iter-metrics')
def report_all_game_iter_metrics():
    """
    This is a rudimentary endpoint that App Engine cron hits to trigger
    the sending of metrics that require iterating through the entire list
    of fresh games.
    """
    games = models.GameListing.query()

    counters = Counter()
    for game in games:
        counters['all_game_listings'] += 1
        if not game.is_fresh():
            continue
        counters['fresh_game_listings'] += 1

        if game.connected_player_count:
            counters['connected_player_count'] += game.connected_player_count
        if game.total_player_count:
            counters['total_player_count'] += game.total_player_count

    EvenniaPlayerConnected.write_gauge(counters['connected_player_count'])
    EvenniaPlayersAll.write_gauge(counters['total_player_count'])
    EDGGameListingsAll.write_gauge(counters['all_game_listings'])
    EDGGameListingsFresh.write_gauge(counters['fresh_game_listings'])

    return "OK"
