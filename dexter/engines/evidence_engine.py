from dexter.core.base_engine import BaseEngine
import requests


class EvidenceEngine(BaseEngine):

    def run(self, target):
        evidence = []

        try:
            response = requests.get(target, timeout=10, allow_redirects=True)

            server = response.headers.get("Server")
            powered = response.headers.get("X-Powered-By")

            if server:
                evidence.append({
                    "engine": "header",
                    "type": "server",
                    "value": server,
                    "confidence": 40,
                })

            if powered:
                evidence.append({
                    "engine": "header",
                    "type": "powered",
                    "value": powered,
                    "confidence": 30,
                })

            for cookie in response.cookies:
                evidence.append({
                    "engine": "cookie",
                    "type": "cookie",
                    "value": f"{cookie.name}={cookie.value}",
                    "confidence": 20,
                })
        except Exception:
            pass

        return evidence