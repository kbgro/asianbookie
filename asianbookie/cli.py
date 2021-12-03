"""Console script for asianbookie."""
import json
import logging
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional

import click
import requests

from . import asianbookie, settings, util
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

    logger.info("[^] openbets3")
    data = load_cache()
    if data is None or data.get("user_bets") is None:
        top_tipsters_response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)
        users = asianbookie.top_tipsters(top_tipsters_response, top100_limit=50)
        matches_ = asianbookie.upcoming_matches()
        users_ranks = asianbookie.matches_bet_users(matches_)
        ab_users_ranks = set(filter(lambda ab_user: ab_user.rank in users_ranks, users))
        user_bets = asianbookie.tipsters_open_bets(ab_users_ranks)
        data = data or {}
        data["user_bets"] = user_bets
        save_cache(data)
    else:
        user_bets = data.get("user_bets")

    user_big_bets = asianbookie.filter_big_bets(user_bets)
    user_big_bets_str = {str(k): v for k, v in user_big_bets.items()}
    logger.debug(f"{json.dumps(user_big_bets_str, default=str)}")

    process_bets(user_big_bets)
    save_bets(user_big_bets_str)
    logger.info("[*] Finishing Application")
    return 0


@asianbookie_cli.command()
def matches():
    """Fetch asianbookie upcoming matches"""

    logger.info("[^] Searching for matches")
    data = load_cache()
    if data is None or data.get("matches") is None:
        matches_ = asianbookie.upcoming_matches()
        data = data or {}
        data["matches"] = matches_
        save_cache(data)
    else:
        matches_ = data.get("matches")

    for match in matches_:
        match.start = match.start + (datetime.now() - datetime.utcnow())
        logger.info(f"[>] {match}")
    logger.info("[*] Finishing Application")

    return 0


def process_bets(bets: asianbookie.UserBets) -> None:
    """
    Get user open bets

    :param bets: open bets
    :return: user's Open bets
    """
    bet_markets = defaultdict(list)
    for bet_list in bets.values():
        for bet in bet_list:
            bet_markets[bet.home + " v " + bet.away].append(bet.market)

    # most common
    print("[^] Open bets")
    for match, bet_m in bet_markets.items():
        mc = Counter(bet_m).most_common()
        logger.debug(f"{match:>40} : {mc}")
        print(f"{match:>40} : {mc}")


def save_bets(bets: asianbookie.UserBets, filename: Optional[str] = None) -> None:
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


def load_cache() -> Optional[Dict]:
    data = util.unpickle_data()
    data = util.unpickle_data()
    if data is not None:
        expire = data.get("expire")  # type: datetime
        logger.info(f"Loading from cache: {expire=}")
        if expire < datetime.now():
            return None
    return data


def save_cache(data: Dict, expire=3600):
    data["created"] = datetime.now()
    data["expire"] = datetime.now() + timedelta(seconds=expire)
    util.pickle_data(data)
