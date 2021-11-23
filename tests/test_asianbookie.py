#!/usr/bin/env python

"""Tests for `asianbookie` package."""

import pytest
from click.testing import CliRunner

from asianbookie import cli
from asianbookie.asianbookie import top10_leagues, top100
from asianbookie.user import AsianBookieUser


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.asianbookie_cli)
    assert result.exit_code == 0
    assert "asianbookie-cli" in result.output
    help_result = runner.invoke(cli.asianbookie_cli, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


# def test_top_tipsters_open_bets():
#     AsianBookieOpenBets(10).top_tipsters_open_bets()


def test_top100():
    users = top100()
    assert isinstance(users, list)
    assert len(users) == 1000
    assert isinstance(users[0], AsianBookieUser)
    assert users[0].user_id


def test_top10_leagues():
    league_users = top10_leagues()
    first_league = list(league_users.values())[0]
    assert league_users
    assert isinstance(league_users, dict)
    assert isinstance(first_league, list)
    assert len(first_league) == 10
    assert isinstance(first_league[0], AsianBookieUser)
    assert first_league[0].user_id


# def test_top_tipsters_open_bets(capsys):
# caplog.set_level(logging.INFO, logger="asianbookie")
# open_bets = AsianBookieOpenBets(5)
# open_bets.top_tipsters_open_bets()

# assert "Fetching bets for:" not in caplog.text
# captured = capsys.readouterr()
# assert captured.out == "[^] Open bets"
