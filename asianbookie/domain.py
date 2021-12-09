from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import List, Optional

from asianbookie import util


class AsianBookieUser:
    """Represents a User in AsianBookie.com"""

    def __init__(self, name, **kwargs):
        self._id: Optional[str] = None
        self._url = ""
        self.name = name
        self.rank: int = 0
        self.win: float = 0.0
        self.draw: float = 0.0
        self.loss: float = 0.0
        self.win_percentage: float = 0.0
        self.win_percentage_big_bet: float = 0.0
        self.yield_: int = 0
        self.longest_winning_streak: int = 0
        self.current_winning_streak: int = 0
        self.recent_form: List[str] = []
        self.balance: float = 0.0
        self.followers: int = 0
        self.current_losing_streak: int = 0
        self.longest_losing_streak: int = 0
        self.member_since: Optional[date] = None

        self.from_kwargs(self, **kwargs)

    def __str__(self):
        return f"AsianBookieUser(name={self.name}, rank={self.rank})"

    def __repr__(self):
        return f"< {self.__str__()} >"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, AsianBookieUser) and other is not None:
            return self.name == other.name and self.user_id == other.user_id
        return False

    def __hash__(self) -> int:
        return hash((self.name, self.user_id))

    @property
    def user_id(self):
        """Return User Id"""
        return self._id

    @property
    def url(self) -> str:
        """Return User URL"""
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._id = util.parse_player_id_from_url(value)

    @classmethod
    def from_top10_league(cls, name: str, rank: int, url: str, balance: float) -> AsianBookieUser:
        user = cls(name)
        user.url = url
        user.rank = rank
        user.balance = balance
        return user

    @classmethod
    def from_top100(cls, name: str, rank: int, url: str, balance: float, **kwargs) -> AsianBookieUser:
        user = cls.from_top10_league(name, rank, url, balance)
        return cls.from_kwargs(user, **kwargs)

    @classmethod
    def from_profile(cls, name: str, rank: int, url: str, balance: float, followers: int, **kwargs) -> AsianBookieUser:
        user = cls.from_top100(name, rank, url, balance)
        user.followers = followers
        return cls.from_kwargs(user, **kwargs)

    @staticmethod
    def from_kwargs(user, **kwargs) -> AsianBookieUser:
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise AttributeError
        return user


class Bet:
    def __init__(
        self,
        placed_at: str,
        team_a: str,
        team_b: str,
        market: str,
        odds: float,
        stake: float,
        status: str,
        league: str,
        is_big_bet: bool,
    ):
        self.placed_at = placed_at
        self.home = team_a
        self.away = team_b
        self.market = market
        self.odds = odds
        self.stake = stake
        self.status = status
        self.league = league
        self.is_big_bet = is_big_bet
        self.user: Optional[AsianBookieUser] = None
        self.match: Optional[Match] = None

    def __str__(self):
        return f"Bet({self.away}, {self.home}, {self.market}, {self.league})"

    def __repr__(self):
        return f"< {self.__str__()} >"

    def __eq__(self, other):
        if (
            isinstance(other, Bet)
            and self.home == other.home
            and self.away == other.away
            and self.league == other.league
            and self.market == other.market
            and self.match.id == other.match.id
            and self.user.user_id == other.user.user_id
        ):
            return True

        return False

    def __hash__(self):
        return hash((self.home, self.away, self.market, self.match.id, self.league, self.user.user_id))

    @property
    def bet_id(self) -> Optional[str]:
        """Returns bet uuid if a bet belong to a user."""
        return uuid.uuid5(uuid.NAMESPACE_X500, f"{self.__str__()}{self.user.user_id}").__str__() if self.user else None


class Match:
    """
    Attributes
    ----------
    id: int
    league: str
    away: str
    home: str
    start: datetime
    ash_away: float
    ash_home: float
    ash_market: str
    over: float
    under: float
    over_under_market: str
    tz: Optional[str]
    summary: dict
    bets: List[Bet]
    """

    def __init__(self, match_id: int, league: str, away: str, home: str, start: datetime, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.id: int = match_id
        self.league: str = league
        self.away: str = away
        self.home: str = home
        self.start: datetime = start
        self.bets: List[Bet] = []

    def __str__(self):
        return f'Match({self.league}, {self.away}, {self.home}, {self.start.strftime("%d/%m/%y %H:%M")})'

    def __repr__(self):
        return f"< {self.__str__()} >"

    def __eq__(self, other):
        if (
            isinstance(other, Match)
            and self.id == other.id
            and self.home == other.home
            and self.away == other.away
            and self.start == other.start
            and self.league == other.league
        ):
            return True
        return False

    def __hash__(self):
        return hash((self.id, self.home, self.away, self.start, self.league))
