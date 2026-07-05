from rich.table import Table

from dexter.ui.console import console


def modules(

        results

):

    table = Table(

        title="Modules"

    )

    table.add_column(

        "Engine"

    )

    table.add_column(

        "Status"

    )

    for k in results:

        if k in [

            "target",

            "mode",

            "technologies"

        ]:

            continue

        table.add_row(

            k,

            "[green]✓[/green]"

        )

    console.print(

        table

    )