"""Console script for asianbookie."""
import json
import logging
import time
from collections import Counter, defaultdict
from itertools import chain
from typing import Dict, List, Optional, Set

import click
import requests

from . import asianbookie, settings
from .domain import AsianBookieUser
from .settings import setup

setup()

logger = logging.getLogger("asianbookie")


@click.group()
def asianbookie_cli():
    """asianbookie cli"""
    logger.info("[*] Starting Application")


@asianbookie_cli.command()
def openbets():
    """Fetch asianbookie open bets"""

    logger.info("[^] Searching for Open bets")

    top_tipsters_response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)
    users = set(asianbookie.top100_users(top_tipsters_response)[:50])
    top10league_users = set(
        chain(*asianbookie.top10_leagues(top_tipsters_response).values())
    )  # type: Set[AsianBookieUser]
    users.update(top10league_users)

    user_big_bets = {}
    user_bets = asianbookie.tipsters_open_bets(users)
    for user, bets in user_bets.items():
        big_bets = list(filter(lambda ub: ub.is_big_bet, bets))
        if big_bets:
            user_big_bets[str(user)] = big_bets

    logger.debug(f"{json.dumps(user_big_bets, default=str)}")

    process_bets(user_big_bets)
    save_bets(user_big_bets)
    logger.info("[*] Finishing Application")
    return 0


@asianbookie_cli.command()
def matches():
    """Fetch asianbookie upcoming matches"""

    logger.info("[^] Searching for matches")
    for match in asianbookie.upcoming_matches():
        logger.info(f"[>] {match}")
    logger.info("[*] Finishing Application")
    return 0


def process_bets(bets: Dict[str, List]) -> None:
    """
    Get user open bets

    :param bets: open bets
    :return: user's Open bets
    """
    bet_markets = defaultdict(list)
    bet_odds = defaultdict(set)
    for bet_list in bets.values():
        for bet in bet_list:
            bet_markets[bet.teamA + " v " + bet.teamB].append(bet.market)
            bet_odds[bet.teamA + " v " + bet.teamB].add(bet.odds)

    # most common
    print("[^] Open bets")
    for match, bet_m in bet_markets.items():
        mc = Counter(bet_m).most_common()
        logger.debug(f"{match:>40} : {mc}")
        print(f"{match:>40} : {mc}")


def save_bets(bets: Dict[str, List], filename: Optional[str] = None) -> None:
    """
    Get user open bets

    :param filename: an optional filename to save bets
    :param bets: open bets
    :return: user's Open bets
    """
    if filename is None:
        filename = str(settings.DATA_DIR / time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ".json"

    with open(filename, "w") as rf:
        json.dump(bets, rf, default=str)
