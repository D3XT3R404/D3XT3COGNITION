from dexter.models.technology import Technology


class CorrelationEngine:

    def analyze(

            self,

            findings

    ):

        technologies = []

        ################################

        metadata = findings.get(

            "metadata",

            {}

        )

        generator = metadata.get(

            "generator",

            ""

        ).lower()

        ################################

        if "wordpress" in generator:

            tech = Technology(

                "WordPress"

            )

            tech.confidence = 98

            tech.version = (

                generator

            )

            tech.add(

                "generator"

            )

            technologies.append(

                tech.export()

            )

        ################################

        frameworks = findings.get(

            "framework",

            []

        )

        for item in frameworks:

            technologies.append(

                {

                    "name":

                        item,

                    "confidence":

                        80,

                    "version":

                        None,

                    "evidence":[

                            "framework_engine"

                    ]

                }

            )

        ################################

        return technologies