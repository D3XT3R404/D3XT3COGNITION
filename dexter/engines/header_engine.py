import requests

from dexter.core.base_engine import BaseEngine


class HeaderEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            data = dict(response.headers)
        except Exception:
            pass

        return data