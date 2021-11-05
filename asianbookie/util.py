import re
from typing import List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

from parsel import Selector


def parse_player_url(url_text: str) -> str:
    parse_result = urlparse(url_text)
    parsed_qs = parse_qs(parse_result.query)
    player = parsed_qs.get("player")[0]
    _id = parsed_qs.get("ID")[0]
    return f"{parse_result.path}?{urlencode({'player': player, 'ID': _id})}"


def parse_with_bold(selector: Selector) -> str:
    win_percentage = selector.css("::text").get().strip()
    if not win_percentage:
        win_percentage = selector.css("b::text").get().strip()
    return win_percentage


def get_float_or_int(text: str) -> Optional[float]:
    found = re.findall(r"\d+\.?\d*", text)
    if found:
        return float(str(found[0]).strip())


def clean_text(text: str, include_texts: List[str]) -> str:
    pattern = r"[" + "".join(include_texts) + "]"
    return re.sub(pattern, "", text)
