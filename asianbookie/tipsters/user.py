from __future__ import annotations

from datetime import date
from typing import List, Optional


class AsianBookieUser:
    def __init__(self, name):
        self.name = name
        self.url: Optional[str] = None
        self._id: Optional[str] = None
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

    def __repr__(self):
        return f"< AsianBookieUser(name={self.name}, rank={self.rank}) >"

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
