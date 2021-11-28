import requests

from asianbookie import settings
from asianbookie.domain import AsianBookieUser
from asianbookie.parsers import OpenBetsParser, match_bets_user_ranks


def test_parse(matches, top100users):
    match = matches[0]

    users_ranks = match_bets_user_ranks(match)
    rank = min(users_ranks)
    user = top100users[rank]  # type: AsianBookieUser
    response = requests.get(f"{settings.ASIAN_BOOKIE_URL}/{user.url}")

    assert response.status_code == 200
    bets = OpenBetsParser.parse(response.text, user)
    bet = bets[0]
    assert bet.user == user
    match.bets = bets
    assert isinstance(bets, list)
