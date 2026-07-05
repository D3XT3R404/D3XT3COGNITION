class Technology:

    def __init__(

            self,

            name

    ):

        self.name = name

        self.version = None

        self.confidence = 0

        self.evidence = []

    def add(

            self,

            item

    ):

        self.evidence.append(

            item

        )

    def score(

            self,

            value

    ):

        self.confidence += value

    def export(

            self

    ):

        return {

            "name":

                self.name,

            "version":

                self.version,

            "confidence":

                self.confidence,

            "evidence":

                self.evidence

        }