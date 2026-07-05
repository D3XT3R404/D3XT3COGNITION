class EvidenceEngine:

    def __init__(

            self

    ):

        self.data = []

    def add(

            self,

            technology,

            source,

            value

    ):

        self.data.append(

            {

                "technology":

                    technology,

                "source":

                    source,

                "value":

                    value

            }

        )

    def export(

            self

    ):

        return self.data