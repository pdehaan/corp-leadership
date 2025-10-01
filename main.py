import json
from itertools import batched

import httpx
from parsel import Selector


def get_leadership():
    res = httpx.get("https://www.adobe.com/about-adobe/leaders.html")
    selector = Selector(text=res.text)

    _parent = "main div.editorial-card.media-square"
    leaders = selector.css(f"""
        {_parent} h2 > a::text,
        {_parent} p::text
    """).getall()

    return [{"name": name, "title": title} for name, title in batched(leaders, 2)]


def main():
    leadership = get_leadership()
    print(json.dumps(leadership, indent=2))


if __name__ == "__main__":
    main()
