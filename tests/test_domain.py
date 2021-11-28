import requests

from asianbookie import settings
from asianbookie.domain import AsianBookieUser, Bet
from asianbookie.parsers import OpenBetsParser, match_bets_user_ranks


def test_bet(matches, top100users):
    match = matches[0]
    users_ranks = match_bets_user_ranks(match)
    rank = min(users_ranks)
    user = top100users[rank]  # type: AsianBookieUser
    response = requests.get(f"{settings.ASIAN_BOOKIE_URL}/{user.url}")
    assert response.status_code == 200
    bet = OpenBetsParser.parse(response.text, user)[0]
    assert str(bet) == f"Bet({bet.away}, {bet.home}, {bet.market}, {bet.league})"
    assert repr(bet) == f"< Bet({bet.away}, {bet.home}, {bet.market}, {bet.league}) >"
    assert bet != match

    bet1 = Bet("15 mins ago", "Ajax", "Sparta", "0:0", 1.56, 100_000, "PENDING", "Dutch Eredevise", True)
    bet1.user = user
    bet1.match = match
    bet2 = Bet("2 hours ago", "Chelsea", "Arsenal", "-1/2:0", 2.56, 10_000, "PENDING", "English Premier League", False)
    bet2.user = user
    bet2.match = match
    assert bet != match
    assert bet1 != bet2
    assert hash(bet1) != hash(bet2)
