from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dexter.ui.console import console


def _tech_rows(results):
    technologies = results.get("technology", []) or []
    versions = results.get("versions", {}) or {}
    confidence = results.get("confidence", {}) or {}

    rows = []
    for tech in technologies:
        conf = confidence.get(str(tech).lower())
        rows.append(
            {
                "name": tech,
                "version": versions.get(tech, "-"),
                "confidence": f"{conf}%" if conf is not None else "-",
            }
        )
    return rows


def _security_score(security_headers):
    if not security_headers:
        return None, None
    present = sum(1 for v in security_headers.values() if v != "Missing")
    total = len(security_headers)
    return present, total


def render_scan(target, results):
    console.print()

    console.print(
        Panel.fit(
            Text.from_markup(
                "[bold cyan]DEXTER[/bold cyan]  [dim]//[/dim]  D3XT3COGNITION\n"
                "[white]Deep Website Information Gathering Framework[/white]"
            ),
            border_style="cyan",
            box=box.ROUNDED,
        )
    )
    console.print()

    # ---- Target summary ----------------------------------------------
    technologies = results.get("technology", []) or []
    versions = results.get("versions", {}) or {}
    framework = results.get("framework")
    emails = results.get("emails", []) or []
    endpoints = results.get("endpoints", []) or []
    forms = results.get("forms", []) or []
    subdomains = (results.get("subfinder", {}) or {}).get("subdomains", []) if isinstance(results.get("subfinder"), dict) else []
    security_headers = results.get("security_headers", {}) or {}
    present, total = _security_score(security_headers)

    summary = Table(title="Target Summary", box=box.SIMPLE_HEAVY, show_lines=False)
    summary.add_column("Field", style="cyan", no_wrap=True)
    summary.add_column("Value", style="green")

    summary.add_row("Target", target)
    summary.add_row("Technologies", str(len(technologies)))
    summary.add_row("Framework", framework or "-")
    summary.add_row("Emails found", str(len(emails)))
    summary.add_row("Endpoints found", str(len(endpoints)))
    summary.add_row("Forms found", str(len(forms)))
    if subdomains:
        summary.add_row("Subdomains", str(len(subdomains)))
    if total:
        ratio_style = "green" if present == total else ("yellow" if present else "red")
        summary.add_row("Security headers", f"[{ratio_style}]{present}/{total} present[/{ratio_style}]")

    console.print(summary)
    console.print()

    # ---- Technologies ---------------------------------------------------
    tech_rows = _tech_rows(results)
    if tech_rows:
        tech_table = Table(title="Technologies Detected", box=box.SIMPLE_HEAVY)
        tech_table.add_column("Name", style="green")
        tech_table.add_column("Version", style="cyan")
        tech_table.add_column("Confidence", justify="right", style="magenta")
        for row in sorted(tech_rows, key=lambda r: r["name"].lower()):
            tech_table.add_row(row["name"], str(row["version"]), row["confidence"])
        console.print(tech_table)
        console.print()

    # ---- Security headers -----------------------------------------------
    if security_headers:
        sec = Table(title="Security Headers", box=box.SIMPLE_HEAVY)
        sec.add_column("Header", style="cyan")
        sec.add_column("Status")
        for header, status in security_headers.items():
            if status == "Missing":
                sec.add_row(header, "[red]Missing[/red]")
            else:
                sec.add_row(header, f"[green]{status}[/green]")
        console.print(sec)
        console.print()

    # ---- Emails -----------------------------------------------------------
    if emails:
        console.print(
            Panel(
                "\n".join(sorted(set(emails))),
                title=f"Emails ({len(emails)})",
                border_style="green",
                box=box.ROUNDED,
            )
        )
        console.print()

    # ---- Interesting endpoints --------------------------------------------
    interesting_keywords = ("admin", "login", "xmlrpc", "wp-json", "api", "graphql", "swagger", "config", "backup")
    interesting = [ep for ep in endpoints if any(k in str(ep).lower() for k in interesting_keywords)]

    if interesting:
        console.print(
            Panel(
                "\n".join(interesting[:20]),
                title=f"Interesting Endpoints ({len(interesting)})",
                border_style="yellow",
                box=box.ROUNDED,
            )
        )
        console.print()

    console.print("[bold green]:heavy_check_mark: Scan Completed[/bold green]")


def reports(target, results=None):
    if results is None:
        results = {}

    return render_scan(target, results)
