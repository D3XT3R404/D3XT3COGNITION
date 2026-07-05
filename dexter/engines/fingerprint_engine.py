from dexter.core.base_engine import BaseEngine
from dexter.core.fingerprint_loader import FingerprintLoader


class FingerprintEngine(BaseEngine):

    name = "fingerprints"

    def run(self, context):

        loader = FingerprintLoader()

        fps = loader.load()

        html = ""

        if context.response:
            html = context.response.text.lower()

        found = []

        for fp in fps:

            if not fp:
                continue

            keywords = fp.get(
                "keywords",
                []
            )

            for keyword in keywords:

                if keyword.lower() in html:

                    found.append(

                        fp["name"]

                    )

                    break

        return sorted(

            set(found)

        )