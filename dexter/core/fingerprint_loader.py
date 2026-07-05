from pathlib import Path

import yaml


class FingerprintLoader:

    def __init__(self):

        self.base = Path(

            "dexter/fingerprints"

        )

    def load(

            self,

            category

    ):

        fingerprints = []

        path = self.base / category

        if not path.exists():

            return []

        for file in path.glob(

                "*.yaml"

        ):

            try:

                with open(

                        file,

                        encoding="utf-8"

                ) as f:

                    data = yaml.safe_load(

                        f

                    )

                    fingerprints.append(

                        data

                    )

            except:

                pass

        return fingerprints