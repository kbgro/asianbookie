import locale
import re
from contextlib import contextmanager
from typing import List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

from parsel import Selector


def parse_player_url(url_text: str) -> str:
    parse_result = urlparse(url_text)
    parsed_qs = parse_qs(parse_result.query)
    player = parsed_qs.get("player")[0]
    _id = parsed_qs.get("ID")[0]
    return f"{parse_result.path}?{urlencode({'player': player, 'ID': _id})}"


def parse_player_id_from_url(url_text: str) -> int:
    """
    Extract user id from user profile link

    :param url_text: user link
    :return: user id
    """
    parsed_qs = parse_qs(urlparse(url_text).query)
    return int(parsed_qs.get("ID")[0])


def parse_with_bold(selector: Selector) -> Optional[str]:
    try:
        win_percentage = selector.css("::text").get().strip()
        if not win_percentage:
            win_percentage = selector.css("b::text").get().strip()
    except AttributeError:
        return None
    return win_percentage


def get_float_or_int(text: str) -> Optional[float]:
    found = re.findall(r"\d+\.?\d*", text)
    if found:
        return float(str(found[0]).strip())


def clean_text(text: str, include_texts: List[str]) -> str:
    pattern = r"[" + "".join(include_texts) + "]"
    return re.sub(pattern, "", text)


def fill_recent_form(recent_form: List[str]) -> List[str]:
    form_map = {"/iconwin.gif": "W", "/icondraw.gif": "D", "/iconlose.gif": "L"}
    return list(map(lambda x: form_map.get(x), recent_form))


@contextmanager
def override_locale(category, locale_string):
    prev_locale_string = locale.getlocale()
    locale.setlocale(category, locale_string)
    yield
    locale.setlocale(category, prev_locale_string)


@override_locale(locale.LC_ALL, "en_US.UTF8")
def parse_balance_text(balance: str) -> float:
    return locale.atof(balance.strip("AB$"))
