import json


class JSONReport:

    def save(

            self,

            directory,

            data

    ):

        with open(

                directory /

                "report.json",

                "w",

                encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )