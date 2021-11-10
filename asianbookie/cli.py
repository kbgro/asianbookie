"""Console script for asianbookie."""
import logging

import click

from asianbookie.asianbookie import AsianBookieOpenBets
from asianbookie.settings import setup

setup()

logger = logging.getLogger("asianbookie")


@click.group()
def asianbookie_cli():
    """asianbookie cli"""


@asianbookie_cli.command()
def openbets():
    """Fetched asianbookie open bets"""
    logger.info("[*] Starting Application")
    logger.info("[^] Searching for Open bets")
    AsianBookieOpenBets().top_tipsters_open_bets()
    logger.info("[*] Finishing Application")
    return 0
