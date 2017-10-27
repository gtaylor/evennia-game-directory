from collections import Counter

from egi import models, app
from egi.metrics.metric_defines import EvenniaPlayerConnected, \
    EvenniaPlayersAll, EDGGameListingsAll, EDGGameListingsFresh, GamePlayersAll, \
    GamePlayersConnected


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
        game_labels = {'game_key_name': game.key.id()}
        counters['all_game_listings'] += 1
        if not game.is_fresh():
            continue
        counters['fresh_game_listings'] += 1

        if game.connect_account_count:
            counters['connected_account_count'] += game.connected_account_count
            GamePlayersConnected.write_gauge(game.connected_account_count, labels=game_labels)
        if game.total_account_count:
            counters['total_account_count'] += game.total_account_count
            GamePlayersAll.write_gauge(game.total_account_count, labels=game_labels)

    EvenniaPlayerConnected.write_gauge(counters['connected_account_count'])
    EvenniaPlayersAll.write_gauge(counters['total_account_count'])
    EDGGameListingsAll.write_gauge(counters['all_game_listings'])
    EDGGameListingsFresh.write_gauge(counters['fresh_game_listings'])

    return "OK"
