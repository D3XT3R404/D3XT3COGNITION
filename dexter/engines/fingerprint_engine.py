from dexter.core.fingerprint_loader import (

    FingerprintLoader

)


class FingerprintEngine:

    def __init__(self):

        self.loader = (

            FingerprintLoader()

        )

    def cms(self):

        return self.loader.load(

            "cms"

        )

    def frameworks(self):

        return self.loader.load(

            "frameworks"

        )