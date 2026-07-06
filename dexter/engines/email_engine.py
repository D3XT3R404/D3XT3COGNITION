import re
import requests

from dexter.core.base_engine import BaseEngine


class EmailEngine(BaseEngine):

    def run(self, target):
        emails = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            emails = list(
                set(
                    re.findall(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                        response.text,
                    )
                )
            )
        except Exception:
            pass

        return sorted(emails)