import json

import httpx
from parsel import Selector

from decorators import timer


@timer(name=__file__)
def get_leadership():
    res = httpx.get("https://www.mozilla.org/en-US/about/leadership/")
    selector = Selector(text=res.text)

    data = []
    for r in selector.css("main > section.leadership-section"):
        section = r.css("h2.leadership-title::text").get()
        for c in r.css("h2 ~ section"):
            data.append(
                {
                    "title": section,
                    "subtitle": c.css("h2.group-title::text").get(),
                    "people": [
                        {
                            "name": p.css(
                                "figure.headshot > figcaption > h3::text"
                            ).get(),
                            "title": p.css(
                                "div.person-info > p[itemprop=jobTitle]::text"
                            ).get(),
                        }
                        for p in c.css("div.gallery > div.vcard")
                    ],
                }
            )
    return data


leadership = get_leadership()
print(json.dumps(leadership, indent=2, ensure_ascii=False))
