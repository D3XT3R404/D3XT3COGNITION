from bs4 import BeautifulSoup
from urllib.parse import urljoin

from dexter.core.base_engine import BaseEngine


class EndpointEngine(BaseEngine):

    TAGS = {
        "a": "href",
        "script": "src",
        "link": "href",
        "img": "src",
        "iframe": "src",
        "source": "src",
        "form": "action",
    }

    def run(self, target):
        endpoints = set()

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
            soup = BeautifulSoup(response.text, "html.parser")

            for tag, attr in self.TAGS.items():
                for node in soup.find_all(tag):
                    value = node.get(attr)
                    if value:
                        endpoints.add(urljoin(response.url, value))
        except Exception:
            pass

        return sorted(endpoints)
