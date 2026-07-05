from dexter.core.base_engine import BaseEngine


class EvidenceEngine(BaseEngine):

    name = "evidence"

    def run(self, context):

        evidence = []

        headers = context.headers

        if "Server" in headers:

            evidence.append({

                "engine": "header",

                "type": "server",

                "value": headers["Server"],

                "confidence": 40

            })

        if "X-Powered-By" in headers:

            evidence.append({

                "engine": "header",

                "type": "powered",

                "value": headers["X-Powered-By"],

                "confidence": 30

            })

        for cookie in context.cookies:

            evidence.append({

                "engine": "cookie",

                "type": "cookie",

                "value": cookie,

                "confidence": 20

            })

        context.evidence = evidence

        return evidence