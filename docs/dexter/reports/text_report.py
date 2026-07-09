class TextReport:

    def save(

            self,

            directory,

            data

    ):

        with open(

                directory /

                "report.txt",

                "w",

                encoding="utf-8"

        ) as f:

            for key, value in data.items():

                f.write(

                    f"{key}\n"

                )

                f.write(

                    f"{value}\n\n"

                )