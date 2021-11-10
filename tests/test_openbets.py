import requests

from asianbookie.openbets import OpenBetsParser


def test_parse():
    # response = requests.get("https://tipsters.asianbookie.com/index.cfm?player=TungChua102&ID=354725")
    response = requests.get("https://tipsters.asianbookie.com/index.cfm?player=teoem115&ID=309283")
    bets = OpenBetsParser.parse(response.text)
    assert isinstance(bets, list)
