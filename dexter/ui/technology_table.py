from rich.table import Table

from dexter.ui.console import console


def technologies(

        data

):

    table = Table(

        title="Technologies"

    )

    table.add_column(

        "Name"

    )

    table.add_column(

        "Confidence"

    )

    table.add_column(

        "Version"

    )

    for tech in data:

        table.add_row(

            tech.get(

                "name",

                ""

            ),

            str(

                tech.get(

                    "confidence",

                    ""

                )

            ),

            str(

                tech.get(

                    "version",

                    ""

                )

            )

        )

    console.print(

        table

    )