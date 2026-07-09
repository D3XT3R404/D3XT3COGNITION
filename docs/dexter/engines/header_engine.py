from dexter.core.base_engine import BaseEngine


class HeaderEngine(BaseEngine):

    def run(self, target):
        data = {}

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None
            data = dict(response.headers)
            if hasattr(target, "headers"):
                target.headers = data
        except Exception as exc:
            if hasattr(target, "errors"):
                target.errors.append(str(exc))

        return data
