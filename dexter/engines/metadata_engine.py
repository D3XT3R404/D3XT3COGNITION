from bs4 import BeautifulSoup
import requests

from dexter.core.base_engine import BaseEngine


class MetadataEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            soup = BeautifulSoup(response.text, "html.parser")

            title = ""
            if soup.title and soup.title.text:
                title = soup.title.text.strip()

            metas = {}
            for meta in soup.find_all("meta"):
                key = meta.get("name") or meta.get("property")
                value = meta.get("content")
                if key and value:
                    metas[key] = value

            data = {
                "title": title,
                "meta": metas,
            }
        except Exception:
            pass

        return data