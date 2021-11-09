"""Main module."""
from __future__ import annotations

import json
import logging
import time
from collections import Counter, defaultdict
from typing import Dict, List, Optional

import requests
from requests import Response

from asianbookie import settings, tipsters
from asianbookie.openbets import Bet, OpenBetsParser
from asianbookie.tipsters import AsianBookieUser

logger = logging.getLogger("asianbookie")


def top100(response: Optional[Response] = None) -> List[AsianBookieUser]:
    """
    Returns a list of top 100 Asian bookie users

    :return: top 100 users
    """
    if response is None:
        response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)
    return tipsters.Top100TipsterParser.parse_top100(response.text)


def top10_leagues(response: Optional[Response] = None) -> Dict[str, List[AsianBookieUser]]:
    """
    Returns a dictionary of a list of top 10 Asian bookie users in that league

    :return: dictionary of league and user list
    """
    if response is None:
        response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)
    return tipsters.Top10LeagueTipsterParser.parse_leagues(response.text)


class AsianBookieOpenBets:
    """
    Collects Open bets for all best tipsters.
    """

    def __init__(self):
        self.top_tipsters_response = requests.get(settings.ASIAN_BOOKIE_TOP_TIPSTERS_URL)

    def top_tipsters_open_bets(self):
        top50 = top100(self.top_tipsters_response)[:50]
        users = set()
        users.update(top50)
        for league in top10_leagues(self.top_tipsters_response).values():
            users.update(league)

        logger.info(f"Fetching bets for: {len(users)} Users")

        # get user bets
        bets = {}
        for index, user in enumerate(users):
            logger.info(f"[R{index:>3d}] Collecting user bets for: [{user.name}:{user.user_id}]")

            user_bets = self.get_user_open_bets(user.url)
            big_bets = list(filter(lambda ub: ub.is_big_bet, user_bets))
            if big_bets:
                bets[str(user)] = big_bets

            logger.debug(f"[R{index:>3d}] [{user.name}:{user.user_id}] : {user_bets}")
            logger.info(f"[R{index:>3d}] [{user.name}:{user.user_id}] : {len(user_bets):2d} bets")
            logger.info(f"[R{index:>3d}] [{user.name}:{user.user_id}] : {len(user_bets):2d} BIG BETS")

            time.sleep(0.5)

        logger.debug(f"{json.dumps(bets, default=str)}")

        self.save_bets(bets)
        self.process_bets(bets)

    @staticmethod
    def get_user_open_bets(user_url: str) -> List[Bet]:
        """
        Get user open bets

        :param user_url: user link url
        :return: user's Open bets
        """
        response = requests.get(f"{settings.ASIAN_BOOKIE_URL}/{user_url}")
        return OpenBetsParser.parse(response.text)

    @staticmethod
    def save_bets(bets: Dict[str, List]) -> None:
        """
        Get user open bets

        :param bets: open bets
        :return: user's Open bets
        """
        filename = settings.DATA_DIR / time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".json"
        with open(filename, "w") as rf:
            json.dump(bets, rf, default=str)

    @staticmethod
    def process_bets(bets: Dict[str, List]) -> None:
        """
        Get user open bets

        :param bets: open bets
        :return: user's Open bets
        """
        bet_markets = defaultdict(list)
        for bet_list in bets.values():
            for bet in bet_list:
                bet_markets[bet.teamA + " v " + bet.teamB].append(bet.market)

        # most common
        for match, bet_m in bet_markets.items():
            mc = Counter(bet_m).most_common()
            logger.debug(f"{match:>40} {mc}")
            print(f"{match:>40} {mc}")
