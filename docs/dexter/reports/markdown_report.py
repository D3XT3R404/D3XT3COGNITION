class MarkdownReport:

    def save(

            self,

            directory,

            data

    ):

        with open(

                directory /

                "report.md",

                "w",

                encoding="utf-8"

        ) as f:

            f.write(

                "# DEXTER Report\n\n"

            )

            for k, v in data.items():

                f.write(

                    f"## {k}\n\n"

                )

                f.write(

                    f"```text\n"

                )

                f.write(

                    str(v)

                )

                f.write(

                    "\n```\n\n"

                )