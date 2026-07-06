import requests

from dexter.core.base_engine import BaseEngine


class CookieEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)

            for cookie in response.cookies:
                data[cookie.name] = cookie.value
        except Exception:
            pass

        return data