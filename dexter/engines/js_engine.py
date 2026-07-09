from bs4 import BeautifulSoup
from urllib.parse import urljoin

from dexter.core.base_engine import BaseEngine


class JsEngine(BaseEngine):

    def run(self, target):
        scripts = []

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
            soup = BeautifulSoup(response.text, "html.parser")

            for script in soup.find_all("script"):
                src = script.get("src")
                if src:
                    scripts.append(urljoin(response.url, src))
        except Exception:
            pass

        return sorted(set(scripts))
