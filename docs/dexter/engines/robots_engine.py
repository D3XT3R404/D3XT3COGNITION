import requests

from dexter.core.base_engine import BaseEngine


class RobotsEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            base = target.rstrip("/")
            url = base + "/robots.txt"
            response = requests.get(url, timeout=10, allow_redirects=True)

            if response.status_code == 200:
                data["url"] = url
                data["content"] = response.text
        except Exception:
            pass

        return data