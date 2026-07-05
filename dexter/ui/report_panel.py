from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def render_scan(target, results):

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]DEXTER[/bold cyan]\n"
            "D3XT3COGNITION\n"
            "Deep Web Information Gathering Framework",
            border_style="cyan"
        )
    )

    console.print()

    summary = Table(title="Target Summary")

    summary.add_column("Field", style="cyan")
    summary.add_column("Value", style="green")

    summary.add_row("Target", target)

    technologies = results.get("technology", [])
    summary.add_row(
        "Technology",
        ", ".join(technologies) if technologies else "-"
    )

    versions = results.get("versions", {})

    version_text = "\n".join(
        f"{k} {v}" for k, v in versions.items()
    )

    summary.add_row(
        "Versions",
        version_text if version_text else "-"
    )

    framework = results.get("framework")

    summary.add_row(
        "Framework",
        framework if framework else "-"
    )

    emails = results.get("emails", [])

    summary.add_row(
        "Emails",
        str(len(emails))
    )

    endpoints = results.get("endpoints", [])

    summary.add_row(
        "Endpoints",
        str(len(endpoints))
    )

    console.print(summary)

    console.print()

    sec = Table(title="Security Headers")

    sec.add_column("Header")
    sec.add_column("Status")

    for header, status in results.get(
        "security_headers",
        {}
    ).items():

        if status == "Missing":

            sec.add_row(
                header,
                "[red]Missing[/red]"
            )

        else:

            sec.add_row(
                header,
                "[green]OK[/green]"
            )

    console.print(sec)

    console.print()

    if technologies:

        tech = Table(title="Technology")

        tech.add_column("Software")
        tech.add_column("Version")

        for t in technologies:

            tech.add_row(
                t,
                versions.get(t, "-")
            )

        console.print(tech)

    console.print()

    if emails:

        console.print(
            Panel(
                "\n".join(emails),
                title="Emails",
                border_style="green"
            )
        )

    console.print()

    interesting = []

    for ep in endpoints:

        if any(x in ep.lower() for x in [

            "admin",
            "login",
            "xmlrpc",
            "wp-json",
            "api",
            "graphql",
            "swagger"

        ]):

            interesting.append(ep)

    if interesting:

        panel = "\n".join(interesting[:20])

        console.print(
            Panel(
                panel,
                title=f"Interesting Endpoints ({len(interesting)})",
                border_style="yellow"
            )
        )

    console.print()

    console.print(
        "[bold green]✓ Scan Completed[/bold green]"
    )

def reports(target, results=None):
    if results is None:
        results = {}

    return render_scan(target, results)