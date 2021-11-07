from dataclasses import dataclass
from typing import List, Optional

from parsel import Selector

from asianbookie import util


@dataclass
class Bet:
    placed_at: str
    teamA: str
    teamB: str
    market: str
    odds: float
    stake: float
    status: str
    league: str


class OpenBetsParser:
    """Parse Tipster Profile"""

    @staticmethod
    def parse(html_text: str) -> List[Bet]:
        selector = Selector(html_text)
        open_table = selector.css("table.altrow")[1]
        open_table_tr = open_table.css("tr")[1:]
        bets = []
        for tr in open_table_tr:
            td = tr.css("td")
            placed_at: str = util.parse_with_bold(td[0])
            league: str = td[1].css("img::attr(title)").get()
            team_a: str = OpenBetsParser._parse_team(td[1])
            team_b: str = OpenBetsParser._parse_team(td[3])
            market: str = OpenBetsParser._parse_market(td[2])
            odds: float = float(td[5].css("font::text").get().strip())
            stake: float = util.parse_balance_text(td[4].css("font::text").get().strip())
            status: str = "STARTED" if td[6].css("font>span::text").get().strip() != "pending" else "PENDING"

            bet = Bet(
                placed_at=placed_at,
                teamA=team_a,
                teamB=team_b,
                market=market,
                stake=stake,
                status=status,
                odds=odds,
                league=league,
            )
            bets.append(bet)

        return bets

    @staticmethod
    def _parse_underlined(selector: Selector) -> Optional[str]:
        return selector.css("u::text").get().strip()

    @staticmethod
    def _parse_team(selector: Selector) -> Optional[str]:
        try:
            team = "".join([x.strip() for x in selector.css("font::text").getall() if x.strip()])
            if not team:
                team = OpenBetsParser._parse_underlined(selector)
        except AttributeError:
            return None

        return team

    @staticmethod
    def _parse_market(selector: Selector) -> Optional[str]:
        try:
            team = "".join(filter(bool, [x.strip() for x in selector.css("font::text").getall()]))
            if not team:
                team = OpenBetsParser._parse_underlined(selector)
        except AttributeError:
            return None

        return team
