import os
import yaml


class FingerprintLoader:

    def __init__(self):

        self.base = os.path.join(
            os.path.dirname(__file__),
            "..",
            "fingerprints"
        )

    def load(self):

        fingerprints = []

        for root, _, files in os.walk(self.base):

            for file in files:

                if not file.endswith(".yaml"):
                    continue

                path = os.path.join(root, file)

                with open(
                    path,
                    encoding="utf-8"
                ) as f:

                    fingerprints.append(

                        yaml.safe_load(f)

                    )

        return fingerprints