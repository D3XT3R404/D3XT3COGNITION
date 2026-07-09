from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def _short_value(value, limit=180):
    text = str(value)
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def render_deep_warning():
    console.print(
        Panel(
            "[bold yellow]Warning[/bold yellow]\n"
            "Menyescan secara mendalam akan membutuhkan beberapa waktu.\n"
            "Harap bersabar.",
            border_style="yellow",
        )
    )
    console.print()


def _mapping_table(title, data):
    table = Table(title=title)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    if isinstance(data, dict) and data:
        for k, v in data.items():
            if isinstance(v, (list, tuple, set)):
                value = f"{len(v)} item(s)"
            elif isinstance(v, dict):
                value = f"{len(v)} field(s)"
            else:
                value = _short_value(v)
            table.add_row(str(k), value)
    else:
        table.add_row("-", "-")

    return table


def _list_table(title, items):
    table = Table(title=title)
    table.add_column("Item", style="green")

    if isinstance(items, list) and items:
        for item in items[:30]:
            table.add_row(str(item))
        if len(items) > 30:
            table.add_row(f"... and {len(items) - 30} more")
    else:
        table.add_row("-")

    return table


def render_section(section, data):
    console.print(f"[bold cyan][*][/bold cyan] {section}")

    if section in ("header", "cookie", "metadata", "security_headers", "version", "dns", "tls", "robots", "waf", "confidence", "cms", "framework", "wordpress"):
        if isinstance(data, dict):
            console.print(_mapping_table(section.title(), data))
        else:
            console.print(Panel(str(data), title=section.title(), border_style="cyan"))

    elif section in ("technology", "fingerprints", "emails", "comments", "endpoints", "forms", "sitemap", "javascript"):
        if isinstance(data, list):
            console.print(_list_table(section.title(), data))
        else:
            console.print(Panel(str(data), title=section.title(), border_style="cyan"))

    elif section in ("httpx", "whatweb", "wpscan", "wafw00f", "katana", "subfinder"):
        if isinstance(data, dict):
            console.print(_mapping_table(section.upper(), data))
        else:
            console.print(Panel(str(data), title=section.upper(), border_style="cyan"))

    elif section == "knowledge":
        if isinstance(data, list) and data:
            table = Table(title="Knowledge")
            table.add_column("Software")
            table.add_column("Version")
            table.add_column("Matched Spec")
            for item in data:
                table.add_row(
                    str(item.get("software", "-")),
                    str(item.get("version", "-")),
                    str(item.get("matched_spec", "-")),
                )
            console.print(table)
        else:
            console.print(Panel("-", title="Knowledge", border_style="cyan"))

    elif section == "evidence":
        if isinstance(data, list) and data:
            table = Table(title="Evidence")
            table.add_column("Source")
            table.add_column("Type")
            table.add_column("Value")
            table.add_column("Confidence")
            for ev in data[:30]:
                table.add_row(
                    str(ev.get("engine", "-")),
                    str(ev.get("type", "-")),
                    str(ev.get("value", "-")),
                    str(ev.get("confidence", 0)),
                )
            console.print(table)
        else:
            console.print(Panel("-", title="Evidence", border_style="cyan"))

    else:
        console.print(Panel(str(data), title=section, border_style="cyan"))

    console.print()


def render_banner(version: str = "v0.1"):
    console.print(
        Panel.fit(
            f"[bold cyan]DEXTER[/bold cyan]\n"
            f"[magenta]D3XT3COGNITION[/magenta]\n"
            f"[green]Deep Website Information Gathering Framework[/green]\n"
            f"[white]{version}[/white]",
            border_style="cyan",
            padding=(1, 4),
        )
    )
