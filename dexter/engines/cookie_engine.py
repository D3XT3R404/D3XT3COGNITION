from dexter.core.base_engine import BaseEngine


class CookieEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None

            for cookie in response.cookies:
                data[cookie.name] = cookie.value
            if hasattr(target, "cookies"):
                target.cookies = data
        except Exception:
            pass

        return data
