from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from dexter.ui.console import console


def render_banner(version: str = "v0.1"):
    logo = r"""
 ____  _______  _______ _____ _____ ____
|  _ \| ____\ \/ /_   _|___ /|  ___/ ___|
| | | |  _|  \  /  | |   |_ \| |_ | |
| |_| | |___ /  \  | |  ___) |  _|| |___
|____/|_____/_/\_\ |_| |____/|_|   \____|
""".strip("\n")

    title = Text()
    title.append(logo, style="bold cyan")
    title.append("\nD3XT3COGNITION", style="bold magenta")
    title.append(f"  {version}\n", style="bold white")
    title.append("Deep Website Information Gathering Framework", style="bold green")
    title.append("\nRecon -> Fingerprint -> Correlate -> Prepare", style="dim white")

    console.print(
        Panel.fit(
            Align.center(title),
            title="[bold white]DEXTER[/bold white]",
            subtitle="[dim]authorized reconnaissance only[/dim]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 3),
        )
    )
