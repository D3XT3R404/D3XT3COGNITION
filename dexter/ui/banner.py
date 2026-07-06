from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def render_banner(version: str = "v0.1"):

    title = Text()
    title.append("DEXTER", style="bold cyan")
    title.append(f"  {version}\n", style="bold white")
    title.append("D3XT3COGNITION\n", style="bold magenta")
    title.append("Deep Website Information Gathering Framework", style="bold green")

    console.print(
        Panel(
            title,
            border_style="cyan",
            padding=(1, 4),
        )
    )