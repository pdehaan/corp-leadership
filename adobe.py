import json
from itertools import batched

import httpx
from parsel import Selector

from decorators import timer


@timer(name=__file__)
def get_leadership():
    res = httpx.get("https://www.adobe.com/about-adobe/leaders.html")
    selector = Selector(text=res.text)

    leaders = selector.css(f"""
        main div.editorial-card.media-square h2 > a::text,
        main div.editorial-card.media-square p::text
    """).getall()

    return [
        {
            "title": "Adobe Leadership",
            "subtitle": None,
            "people": [
                {"name": name, "title": title} for name, title in batched(leaders, 2)
            ],
        }
    ]


leadership = get_leadership()
print(json.dumps(leadership, indent=2, ensure_ascii=False))
