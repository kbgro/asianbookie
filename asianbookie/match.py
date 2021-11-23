from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from dateutil.parser import parse
from parsel import Selector

from . import util


@dataclass
class Match:
    league: str
    away: str
    home: str
    ash_away: float
    ash_home: float
    ash_market: str
    over: float
    under: float
    over_under_market: str
    start: datetime
    tz: Optional[str]
    summary: dict


class MatchParser:
    @classmethod
    def parse(cls, html_text: str) -> List[Match]:
        matches = []
        tz = Selector(html_text).xpath("//select[@name='timezone']/option[@selected]/text()").get()
        for table in cls._match_tables(html_text):
            match = cls._extract_match(table, tz=tz)
            matches.append(match)
        return matches

    @classmethod
    def _match_tables(cls, html_text: str) -> List[Selector]:
        tables = []
        start = False
        table_lines = []
        for line in html_text.split("\n"):
            table_lines.append(line)
            if line.startswith('<table class="group'):
                if start:
                    tables.append("".join(table_lines[:-1]))
                    table_lines.clear()
                    table_lines.append(line)
                if not start:
                    start = True
                    table_lines.clear()
                    table_lines.append(line)
        tables.append("".join(table_lines[:-1]))

        return list(map(lambda tl: Selector(tl), tables))

    @classmethod
    def _extract_match(cls, table_selector: Selector, tz: Optional[str] = None) -> Match:
        table_row_selectors = table_selector.css("tr")
        # league
        league = util.parse_with_bold(table_row_selectors[0].css("font")[1])

        # home, away teams
        normalized_it = map(lambda t: util.normalize_text(t), table_row_selectors[0].css("font::text").getall())
        match_no, name = list(filter(bool, normalized_it))
        name = name[1:] if name[0] == "-" else name
        home, away = name.split(" v ")

        # odds and markets
        teams_odds = list(
            filter(bool, map(lambda t: util.normalize_text(t), table_row_selectors[3].css("::text").getall()))
        )
        ash, over_under = teams_odds[:-5], teams_odds[-5:]

        # over, under and o/u market
        over, _, over_under_market, _, under = over_under

        # home, away odds and h/a market asian handicap
        market_index = list(filter(lambda x: " : " in x[-1], enumerate(ash)))  # noqa
        index, ash_market = market_index[0]
        ash_home, ash_away = float(ash[index - 1]), float(ash[index + 1])

        # summary
        summary = OrderedDict()
        tl = table_row_selectors[5].css(".ahex ::text").getall()
        tl.extend(table_row_selectors[5].css(".ouex ::text").getall())
        tl = list(filter(lambda t: "Payment Outcome Summary" not in t, tl))
        for k, v in util.chunks(tl, 2):
            summary[k] = v

        # time
        start = list(filter(bool, map(util.normalize_text, table_row_selectors[11].css("::text").getall())))[0]
        start = parse(start, fuzzy_with_tokens=True)[0]  # noqa

        return Match(
            league, away, home, ash_away, ash_home, ash_market, over, under, over_under_market, start, tz, summary
        )
