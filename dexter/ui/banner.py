from rich.panel import Panel

from dexter.ui.console import console


def banner():

    panel = Panel(

        "[bold cyan]D3XT3COGNITION[/bold cyan]\n"

        "Deep Reconnaissance Framework",

        expand=False

    )

    console.print(

        panel

    )