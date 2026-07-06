from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

from dexter.core.base_engine import BaseEngine


class JsEngine(BaseEngine):

    def run(self, target):
        scripts = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")

            for script in soup.find_all("script"):
                src = script.get("src")
                if src:
                    scripts.append(urljoin(target, src))
        except Exception:
            pass

        return sorted(set(scripts))