import requests

from dexter.core.base_engine import BaseEngine


class SecurityHeadersEngine(BaseEngine):

    SECURITY_HEADERS = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
    ]

    def run(self, target):
        data = {}

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)

            for header in self.SECURITY_HEADERS:
                value = response.headers.get(header)
                data[header] = value if value else "Missing"
        except Exception:
            pass

        return data