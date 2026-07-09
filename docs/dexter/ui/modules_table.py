from rich import box
from rich.table import Table

from dexter.ui.console import console

SKIP_KEYS = {"target", "host", "technology", "versions", "confidence", "adapters"}


def _status(data):
    if isinstance(data, dict) and data.get("error"):
        error = str(data["error"]).lower()
        if "not found" in error:
            return "[dim]skipped (tool not found)[/dim]"
        return f"[yellow]error: {data['error'][:60]}[/yellow]"

    if isinstance(data, (list, dict)) and not data:
        return "[dim]no data[/dim]"

    return "[green]\u2713 ok[/green]"


def modules(results):
    table = Table(title="Modules", box=box.SIMPLE_HEAVY)

    table.add_column("Engine", style="cyan")
    table.add_column("Status")

    for key, value in results.items():
        if key in SKIP_KEYS:
            continue
        table.add_row(key, _status(value))

    adapters = results.get("adapters")
    if isinstance(adapters, dict):
        for key, value in adapters.items():
            table.add_row(f"adapter:{key}", _status(value))

    console.print(table)
