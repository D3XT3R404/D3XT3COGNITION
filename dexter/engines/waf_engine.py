import requests

from dexter.core.base_engine import BaseEngine


class WafEngine(BaseEngine):

    def run(self, target):
        waf = None

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)
            headers = {k.lower(): str(v).lower() for k, v in response.headers.items()}

            if "cloudflare" in headers.get("server", "") or "cf-ray" in headers:
                waf = "Cloudflare"
            elif "akamai" in headers.get("server", ""):
                waf = "Akamai"
            elif "sucuri" in headers.get("server", ""):
                waf = "Sucuri"
        except Exception:
            pass

        return waf