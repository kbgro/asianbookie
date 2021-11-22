import math
from collections import defaultdict
from typing import Dict, List, Optional

from parsel import Selector

from asianbookie import util
from asianbookie.user import AsianBookieUser


class TipsterProfileParser:
    """Parse Tipster Profile"""

    @staticmethod
    def parse(html_text: str) -> AsianBookieUser:
        selector = Selector(html_text)
        profile_td = selector.css(".lightblue td")
        profile_td_texts = list(filter(bool, map(util.normalize_text, profile_td.css("td::text").getall())))
        b = profile_td.xpath(".//b")
        name = profile_td.css("b>font::text").get()
        followers = b[4].css("::text").get()
        balance = b[6].css("font::text").get()
        rank = int(profile_td_texts[1].split("of")[0].replace("#", "").strip())
        recent_form = list(
            filter(
                lambda i: i.startswith("/icon"),
                map(util.normalize_text, profile_td.css("td img::attr(src)").getall()),
            )
        )
        recent_form = util.fill_recent_form(recent_form)
        user = AsianBookieUser(name)
        user.rank = rank
        user.recent_form = recent_form
        user.followers = followers
        user.balance = util.parse_balance_text(balance)

        return user


class Top100TipsterParser:
    @staticmethod
    def parse_top100(html_text: str) -> List[AsianBookieUser]:
        selector = Selector(html_text)
        tipsters = []
        for tr in selector.css("table.altrow tr")[1:]:
            tip = Top100TipsterParser.parse_tipster_row(tr)
            if tip:
                tipsters.append(tip)
        return tipsters

    @staticmethod
    def parse_tipster_row(tr_selector: Selector) -> Optional[AsianBookieUser]:
        table_data_list = tr_selector.css("td")
        if len(table_data_list) < 2:
            return

        rank = table_data_list[0].css("font::text").get().split(".")[0]
        name = table_data_list[1].css("font>a::text").get()
        url = table_data_list[1].css("font>a::attr(href)").get()
        win = table_data_list[2].css("::text").get().strip()
        draw = table_data_list[3].css("::text").get().strip()
        loss = table_data_list[4].css("::text").get().strip()
        win_percentage = util.parse_with_bold(table_data_list[5])
        win_percentage = util.get_float_or_int(win_percentage) or math.nan
        win_percentage_big_bet = util.parse_with_bold(table_data_list[6])
        win_percentage_big_bet = util.get_float_or_int(win_percentage_big_bet) or math.nan
        yield_ = util.get_float_or_int(table_data_list[7].css("::text").get().strip())
        current_winning_streak = util.get_float_or_int(table_data_list[8].css("span")[1].css("::text").get())
        longest_winning_streak = util.get_float_or_int(table_data_list[8].css("span")[-1].css("::text").get())
        recent_form = list(map(lambda x: x.attrib["src"], table_data_list[9].css("img")))
        recent_form = util.fill_recent_form(recent_form)
        balance = util.parse_with_bold(table_data_list[10].css("font"))
        balance = util.get_float_or_int(util.clean_text(balance, [","]))

        return AsianBookieUser.from_top100(
            name,
            rank,
            util.parse_player_url(url),
            balance,
            win=float(win),
            draw=float(draw),
            loss=float(loss),
            win_percentage=win_percentage,
            win_percentage_big_bet=win_percentage_big_bet,
            yield_=int(yield_),
            longest_winning_streak=int(longest_winning_streak),
            current_winning_streak=int(current_winning_streak),
            recent_form=recent_form,
        )


class Top10LeagueTipsterParser:
    @staticmethod
    def parse_leagues(html_text: str) -> Dict[str, List[AsianBookieUser]]:
        selector = Selector(html_text)
        league_tipsters = defaultdict(list)
        for league in selector.xpath("//table[@height='145']"):
            tr = league.xpath(".//tr")
            league_name = util.parse_with_bold(tr[0].css("a"))
            league_name = league_name.split("Top 10")[-1].strip()

            for t_tr in tr[1:]:
                tip = Top10LeagueTipsterParser.parse_tipster_row(t_tr)
                league_tipsters[league_name].append(tip)
        return league_tipsters

    @staticmethod
    def parse_tipster_row(tr_selector: Selector) -> AsianBookieUser:
        table_data_list = tr_selector.css("td")
        rank = table_data_list[0].css("span::text").get().split(".")[0]
        name = table_data_list[1].css("font>a::text").get().strip()
        url_text = table_data_list[1].css("font>a::attr(href)").get()
        url = util.parse_player_url(url_text)
        balance_text = list(
            filter(bool, map(lambda x: x.strip(), tr_selector.css("td")[2].css("font font::text").getall()))
        )[0]
        balance = util.get_float_or_int(balance_text)

        return AsianBookieUser.from_top10_league(rank=int(rank), url=url, name=name, balance=balance)
