from dexter.core.base_engine import BaseEngine


class EvidenceEngine(BaseEngine):

    def run(self, target):
        evidence = []

        try:
            response = target.fetch(timeout=15) if hasattr(target, "fetch") else None

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
