from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dexter.ui.banner import render_banner

console = Console()


def _safe_join(items, limit=10):
    if not items:
        return "-"
    items = list(items)
    if len(items) > limit:
        items = items[:limit]
        return ", ".join(items) + " ..."
    return ", ".join(items)


def render_scan(target, results, deep: bool = False):

    render_banner()

    console.print()

    summary = Table(title="Target Summary")
    summary.add_column("Field", style="cyan")
    summary.add_column("Value", style="green")

    summary.add_row("Target", target)

    technologies = results.get("technology", [])
    summary.add_row(
        "Technology",
        _safe_join(technologies, 8)
    )

    framework = results.get("framework") or "-"
    summary.add_row("Framework", framework)

    cms = results.get("cms") or "-"
    summary.add_row("CMS", cms)

    versions = results.get("versions", {})
    if versions:
        version_text = "\n".join(f"{k} {v}" for k, v in versions.items())
    else:
        version_text = "-"

    summary.add_row("Versions", version_text)

    emails = results.get("emails", [])
    summary.add_row("Emails", str(len(emails)))

    endpoints = results.get("endpoints", [])
    summary.add_row("Endpoints", str(len(endpoints)))

    console.print(summary)
    console.print()

    sec = Table(title="Security Headers")
    sec.add_column("Header")
    sec.add_column("Status")

    for header, status in results.get("security_headers", {}).items():
        if status == "Missing":
            sec.add_row(header, "[red]Missing[/red]")
        else:
            sec.add_row(header, "[green]OK[/green]")

    console.print(sec)
    console.print()

    tech = Table(title="Technology Stack")
    tech.add_column("Software")
    tech.add_column("Version")

    for t in technologies:
        tech.add_row(
            t,
            versions.get(t, "-")
        )

    if technologies:
        console.print(tech)
        console.print()

    wordpress = results.get("wordpress") or {}
    if wordpress and wordpress.get("detected"):
        wp_panel = Table(title="WordPress Intelligence")
        wp_panel.add_column("Field")
        wp_panel.add_column("Value")

        wp_panel.add_row("Detected", "[green]Yes[/green]")
        wp_panel.add_row("Generator", wordpress.get("generator") or "-")
        wp_panel.add_row("REST API", str(len(wordpress.get("rest_api", []))))
        wp_panel.add_row("XML-RPC", "Yes" if wordpress.get("xmlrpc") else "No")
        wp_panel.add_row("Plugins", _safe_join(wordpress.get("plugins", []), 8))
        wp_panel.add_row("Themes", _safe_join(wordpress.get("themes", []), 8))

        console.print(wp_panel)
        console.print()

    if deep:
        comments = results.get("comments", [])
        if comments:
            comment_panel = Panel(
                "\n".join(
                    f"- {item.get('keyword', '')}: {item.get('comment', '')}"
                    for item in comments[:10]
                ),
                title=f"Comments ({len(comments)})",
                border_style="yellow",
            )
            console.print(comment_panel)
            console.print()

        endpoints = results.get("endpoints", [])
        interesting = []
        for ep in endpoints:
            low = ep.lower()
            if any(x in low for x in [
                "wp-json",
                "xmlrpc",
                "wp-admin",
                "wp-content",
                "wp-includes",
                "admin",
                "login",
                "api",
                "graphql",
                "swagger",
                "feed",
                "sitemap",
            ]):
                interesting.append(ep)

        if interesting:
            interesting_panel = Panel(
                "\n".join(interesting[:20]),
                title=f"Interesting Endpoints ({len(interesting)})",
                border_style="cyan",
            )
            console.print(interesting_panel)
            console.print()

        evidence = results.get("evidence", [])
        if evidence:
            evidence_table = Table(title="Evidence")
            evidence_table.add_column("Source")
            evidence_table.add_column("Type")
            evidence_table.add_column("Value")
            evidence_table.add_column("Confidence")

            for ev in evidence[:20]:
                evidence_table.add_row(
                    ev.get("engine", "-"),
                    ev.get("type", "-"),
                    ev.get("value", "-"),
                    str(ev.get("confidence", 0)),
                )

            console.print(evidence_table)
            console.print()

        knowledge = results.get("knowledge", [])
        if knowledge:
            knowledge_panel = Table(title="Knowledge")
            knowledge_panel.add_column("Software")
            knowledge_panel.add_column("Version")
            knowledge_panel.add_column("Status")
            knowledge_panel.add_column("CVEs")

            for item in knowledge[:10]:
                db = item.get("knowledge", {})
                versions_db = db.get("versions", {})
                matched_status = "-"
                cves = "-"

                if isinstance(versions_db, dict):
                    matched_status = versions_db.get("status", "-")
                    cve_list = versions_db.get("cves", [])
                    if cve_list:
                        if isinstance(cve_list, list):
                            cves = ", ".join(
                                x.get("id", "-") if isinstance(x, dict) else str(x)
                                for x in cve_list
                            )
                        else:
                            cves = str(cve_list)

                knowledge_panel.add_row(
                    item.get("software", "-"),
                    item.get("version", "-"),
                    matched_status,
                    cves,
                )

            console.print(knowledge_panel)
            console.print()

    console.print("[bold green]✓ Scan Completed[/bold green]")