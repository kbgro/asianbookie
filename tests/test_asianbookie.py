#!/usr/bin/env python

"""Tests for `asianbookie` package."""

from click.testing import CliRunner

from asianbookie import cli
from asianbookie.asianbookie import tipsters_open_bets, top10_leagues, top100_users
from asianbookie.domain import AsianBookieUser


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.asianbookie_cli)  # noqa
    assert result.exit_code == 0
    assert "asianbookie-cli" in result.output
    help_result = runner.invoke(cli.asianbookie_cli, ["--help"])  # noqa
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_top100():
    users = top100_users()
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


def test_tipsters_open_bets(top100users):
    top_tipster_bets = tipsters_open_bets((top100users[1], top100users[2]))
    assert len(top_tipster_bets) == 2
