from rich import box
from rich.table import Table

from dexter.ui.console import console


def technologies(data):
    table = Table(title="Technologies", box=box.SIMPLE_HEAVY)

    table.add_column("Name", style="green")
    table.add_column("Confidence", justify="right", style="magenta")
    table.add_column("Version", style="cyan")

    for tech in data:
        table.add_row(
            tech.get("name", ""),
            str(tech.get("confidence", "-")),
            str(tech.get("version", "-")),
        )

    console.print(table)
