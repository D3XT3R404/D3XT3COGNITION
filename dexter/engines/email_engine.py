import re

from dexter.core.base_engine import BaseEngine


class EmailEngine(BaseEngine):

    def run(self, target):
        emails = []

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
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
