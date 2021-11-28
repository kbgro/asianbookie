#!/usr/bin/env python

"""Tests for `tipsters` package."""

import pytest
import requests

from asianbookie.domain import AsianBookieUser
from asianbookie.parsers import (
    TipsterProfileParser,
    Top10LeagueTipsterParser,
    Top100TipsterParser,
)


@pytest.fixture
def response():
    return requests.get("https://tipsters.asianbookie.com/index.cfm?top20=1")


def test_top100_tipsters(response):
    tipsters = Top100TipsterParser.parse_top100(response.text)
    assert isinstance(tipsters, list)
    assert isinstance(tipsters[0], AsianBookieUser)
    assert len(tipsters) == 1000


def test_league_top10_tipsters(response):
    league_tipsters = Top10LeagueTipsterParser.parse_leagues(response.text)
    assert isinstance(league_tipsters, dict)
    assert len(league_tipsters) >= 20


def test_tipster_profile():
    response = requests.get("https://tipsters.asianbookie.com/index.cfm?player=kopikia&ID=382731")
    user = TipsterProfileParser.parse(response.text)
    assert isinstance(user, AsianBookieUser)
    assert user.balance != 0
