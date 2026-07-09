import requests

from dexter.core.base_engine import BaseEngine


class SitemapEngine(BaseEngine):

    def run(self, target):
        data = []

        try:
            base = target.rstrip("/")
            url = base + "/sitemap.xml"
            response = requests.get(url, timeout=10, allow_redirects=True)

            if response.status_code == 200:
                data.append({
                    "url": url,
                    "content": response.text,
                })
        except Exception:
            pass

        return data