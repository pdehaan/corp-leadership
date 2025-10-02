from itertools import batched

import httpx
from parsel import Selector

from decorators import timer


class Adobe:
    slug = "adobe"

    @timer(name=__file__)
    def get_board_of_directors(self):
        URL = "https://www.adobe.com/about-adobe/leaders/board-directors.html"

        res = httpx.get(url=URL)
        html = Selector(text=res.text)

        # HACK: Some board members are H2s and others are H3s. :shrug:
        board = html.css("""
            main div > h2::text,
            main div > h2 ~ p:first-of-type > strong::text,

            main div > h3::text,
            main div > h3 ~ p:first-of-type > strong::text
        """).getall()

        return {
            "title": "Board of Directors",
            "subtitle": None,
            "people": [
                {"name": name, "title": title}
                for name, title in batched(board, n=2, strict=True)
            ],
        }

    @timer(name=__file__)
    def get_leadership(self):
        res = httpx.get(url="https://www.adobe.com/about-adobe/leaders.html")
        html = Selector(text=res.text)

        leaders = html.css("""
            main div.editorial-card.media-square h2 > a::text,
            main div.editorial-card.media-square p::text
        """).getall()

        leadership = {
            "title": "Adobe Leadership",
            "subtitle": None,
            "people": [
                {"name": name, "title": title}
                for name, title in batched(leaders, n=2, strict=True)
            ],
        }

        return [leadership, self.get_board_of_directors()]
