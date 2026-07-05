class EvidenceEngine:

    def __init__(self):

        self.evidence = []

    def add(

            self,

            technology,

            source,

            value

    ):

        self.evidence.append(

            {

                "technology":

                    technology,

                "source":

                    source,

                "value":

                    value

            }

        )

    def get(

            self

    ):

        return self.evidence