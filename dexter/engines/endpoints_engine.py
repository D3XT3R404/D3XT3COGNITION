from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

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
            response = requests.get(target, timeout=10, allow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag, attr in self.TAGS.items():
                for node in soup.find_all(tag):
                    value = node.get(attr)
                    if value:
                        endpoints.add(urljoin(target, value))
        except Exception:
            pass

        return sorted(endpoints)