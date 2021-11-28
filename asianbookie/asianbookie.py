"""Main module."""
from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional, Set

import requests
from requests import Response

from . import parsers, settings
from .domain import AsianBookieUser, Bet

logger = logging.getLogger("asianbookie")


def get_user_open_bets(user: AsianBookieUser) -> List[Bet]:
    """
    Get user open bets

    :param user: AsianBookie user
    :return: user's Open bets
    """
    response = requests.get(f"{settings.ASIAN_BOOKIE_URL}/{user.url}")
    return parsers.OpenBetsParser.parse(response.text, user)


def upcoming_matches():
    """
    Returns upcoming football matches
    :return: a list of matches
    """
    response = requests.get(settings.ASIAN_BOOKIE_URL)
    return parsers.MatchParser.parse(response.text)


def top100_users(response: Optional[Response] = None) -> List[AsianBookieUser]:
    """
    Returns a list of top 100 Asian bookie users

    :return: top 100 users
    """
    if response is None:
        response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)
    return parsers.Top100TipsterParser.parse_top100(response.text)


def top10_leagues(response: Optional[Response] = None) -> Dict[str, List[AsianBookieUser]]:
    """
    Returns a dictionary of a list of top 10 Asian bookie users in that league

    :return: dictionary of league and user list
    """
    if response is None:
        response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)
    return parsers.Top10LeagueTipsterParser.parse_leagues(response.text)


def tipsters_open_bets(tipsters: Set[AsianBookieUser], sleep_time: float = 0.5) -> Dict[AsianBookieUser, List[Bet]]:
    """
    Returns a dictionary of tipsters and a list of their open bets
    :param sleep_time: wait time when fetching multiple users open bets
    :param tipsters: a list of tipster to fetch open bets
    :return: a dictionary of tipsters and a list of their open bets
    """
    logger.info(f"Fetching bets for: {len(tipsters)} Users")

    # get user bets
    user_bets = {}
    for index, user in enumerate(tipsters):
        logger.info(f"[R {index:>3d}] Collecting user bets for: [{user.name}:{user.user_id}]")

        user_bets[user] = get_user_open_bets(user)

        logger.debug(f"[R {index:>3d}] [{user.name}:{user.user_id}] : {user_bets}")
        logger.info(f"[R {index:>3d}] [{user.name}:{user.user_id}] : {len(user_bets):2d} bets")
        logger.info(f"[R {index:>3d}] [{user.name}:{user.user_id}] : {len(user_bets):2d} BIG BETS")

        time.sleep(sleep_time)

    return user_bets
