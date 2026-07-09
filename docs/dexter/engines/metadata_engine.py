from bs4 import BeautifulSoup

from dexter.core.base_engine import BaseEngine


class MetadataEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
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
            if hasattr(target, "metadata"):
                target.metadata = data
        except Exception:
            pass

        return data
