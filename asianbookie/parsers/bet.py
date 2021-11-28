from typing import List

from parsel import Selector

from .. import util
from ..domain import AsianBookieUser, Bet


class OpenBetsParser:
    """Parse Tipster Profile"""

    @staticmethod
    def parse(html_text: str, user: AsianBookieUser) -> List[Bet]:
        bets: List[Bet] = []
        selector = Selector(html_text)
        open_table = selector.css("table.altrow")[1]

        if not OpenBetsParser.has_open_bets(open_table):
            return bets

        open_table_tr = open_table.css("tr")[1:]
        for tr in open_table_tr:
            td = tr.css("td")
            placed_at: str = util.parse_with_bold(td[0])
            league: str = td[1].css("img::attr(title)").get()
            team_a: str = OpenBetsParser._parse_team(td[1])
            team_b: str = OpenBetsParser._parse_team(td[3])
            market: str = OpenBetsParser._parse_market(td[2])
            odds: float = float(td[5].css("font::text").get().strip())
            stake: float = util.parse_balance_text(td[4].css("font::text").get().strip())
            is_big_bet: bool = "bigbet" in (td[4].css("img::attr(src)").get() or "")
            status: str = "STARTED" if td[6].css("font>span::text").get().strip() != "pending" else "PENDING"

            bet = Bet(
                placed_at,
                team_a,
                team_b,
                market,
                odds,
                stake,
                status,
                league,
                is_big_bet,
            )
            bet.user = user
            bets.append(bet)

        return bets

    @staticmethod
    def has_open_bets(open_bet_table: Selector) -> bool:
        first_tr = map(lambda x: x.strip(), open_bet_table.css("tr")[1].css("::text").getall())
        return "currently no pending bets." not in "".join(first_tr)

    @staticmethod
    def _parse_underlined(selector: Selector) -> str:
        return selector.css("u::text").get().strip() or ""

    @staticmethod
    def _parse_team(selector: Selector) -> str:
        try:
            team = "".join([x.strip() for x in selector.css("font::text").getall() if x.strip()])
            if not team:
                team = OpenBetsParser._parse_underlined(selector)
        except AttributeError:
            return ""

        return team

    @staticmethod
    def _parse_market(selector: Selector) -> str:
        try:
            team = "".join(filter(bool, [x.strip() for x in selector.css("font::text").getall()]))
            if not team:
                team = OpenBetsParser._parse_underlined(selector)
        except AttributeError:
            return ""

        return team
