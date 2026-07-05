from rich.panel import Panel

from dexter.ui.console import console


def reports(

        target

):

    txt = (

        f"reports/{target}/\n\n"

        "report.json\n"

        "report.html\n"

        "report.md\n"

        "report.txt"

    )

    console.print(

        Panel(

            txt,

            title="Reports Saved"

        )

    )