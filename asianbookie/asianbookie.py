"""Main module."""
from __future__ import annotations

import logging
import time
from itertools import chain
from typing import Dict, List, Optional, Set

import requests
from requests import Response

from . import parsers, settings
from .domain import AsianBookieUser, Bet, Match

logger = logging.getLogger("asianbookie")

UserBets = Dict[AsianBookieUser, List[Bet]]


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


def match_bet_users(match: Match) -> Set:
    """
    Return user rank of users with bet in a current match
    :param match:
    :return:
    """
    response = requests.get(f"{settings.ASIAN_BOOKIE_URL}/matchstat.cfm?id={match.id}")
    return parsers.MatchBetUsersParser.parse(response.text)


def matches_bet_users(matches: List[Match]) -> Set:
    """
    Return user rank of users with bet in any of the matches

    :param matches: a list of matches
    :return: a set of user ranks
    """
    ranks = set()
    for match in matches:
        ranks.update(match_bet_users(match))
    return ranks


def top_tipsters(response: Response, top100_limit: int = 50) -> Set[AsianBookieUser]:
    """
    Returns a list of top 50 tipsters and top 10 tipsters in leagues

    :param top100_limit: a limit for top 100 tipsters
    :param response: request response
    :return: a list of top tipster
    """
    _all_users = top100_users(response)
    user_map = {user.user_id: user for user in _all_users}  # type: Dict[int, AsianBookieUser]
    top_tens_with_rank = list(map(lambda u: user_map.get(u.user_id), chain(*top10_leagues(response).values())))
    top_tens_filtered = set(filter(bool, top_tens_with_rank))  # type: ignore

    # top_tens_100 = list(filter(lambda u: u.rank <= top100_limit, top_tens))
    users = set(_all_users[:top100_limit])
    users.update(top_tens_filtered)  # type: ignore

    logger.info(f"Top tipsters: {len(users)}")

    return users


def filter_big_bets(user_bets: UserBets) -> UserBets:
    """
    Filter user bets and returns only bet marked `big bet`
    :param user_bets: a dictionary of user and their bets
    :return:  a dictionary of user and their bets
    """
    user_big_bets: UserBets = {}
    for user, bets in user_bets.items():
        big_bets = list(filter(lambda ub: ub.is_big_bet, bets))
        if big_bets:
            user_big_bets[user] = big_bets
    return dict(user_big_bets)
