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


def _print_section(title):
    console.print(f"[bold cyan][*][/bold cyan] {title}")


def _print_mapping(title, data):
    table = Table(title=title)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    if isinstance(data, dict) and data:
        for k, v in data.items():
            table.add_row(str(k), str(v))
    else:
        table.add_row("-", "-")

    console.print(table)
    console.print()


def _print_list(title, items):
    table = Table(title=title)
    table.add_column("Item", style="green")

    if isinstance(items, list) and items:
        for item in items:
            table.add_row(str(item))
    else:
        table.add_row("-")

    console.print(table)
    console.print()


def render_scan(target, results, deep: bool = False):
    render_banner()
    console.print()

    # =========================
    # BASIC SECTIONS
    # =========================

    _print_section("header")
    _print_mapping("Header", results.get("headers", {}))

    _print_section("cookie")
    _print_mapping("Cookie", results.get("cookies", {}))

    _print_section("metadata")
    _print_mapping("Metadata", results.get("metadata", {}))

    _print_section("securityheaders")
    _print_mapping("Security Headers", results.get("security_headers", {}))

    _print_section("technology")
    _print_list("Technology", results.get("technology", []))

    _print_section("framework")
    framework = results.get("framework") or "-"
    console.print(Panel(str(framework), title="Framework", border_style="cyan"))
    console.print()

    _print_section("version")
    _print_mapping("Versions", results.get("versions", {}))

    _print_section("fingerprint")
    _print_list("Fingerprints", results.get("fingerprints", []))

    _print_section("knowledge")
    knowledge = results.get("knowledge", [])
    if isinstance(knowledge, list) and knowledge:
        table = Table(title="Knowledge")
        table.add_column("Software")
        table.add_column("Version")
        table.add_column("Status")
        table.add_column("CVEs")

        for item in knowledge:
            db = item.get("knowledge", {}) if isinstance(item, dict) else {}
            versions_db = db.get("versions", {}) if isinstance(db, dict) else {}
            status = "-"
            cves = "-"

            if isinstance(versions_db, dict):
                status = versions_db.get("status", "-")
                cve_list = versions_db.get("cves", [])
                if isinstance(cve_list, list) and cve_list:
                    cves = ", ".join(
                        x.get("id", "-") if isinstance(x, dict) else str(x)
                        for x in cve_list
                    )

            table.add_row(
                str(item.get("software", "-")),
                str(item.get("version", "-")),
                str(status),
                str(cves),
            )

        console.print(table)
        console.print()
    else:
        console.print(Panel("-", title="Knowledge", border_style="cyan"))
        console.print()

    _print_section("endpoint")
    endpoints = results.get("endpoints", [])
    if endpoints:
        table = Table(title="Endpoints")
        table.add_column("URL")
        for ep in endpoints[:30]:
            table.add_row(ep)
        if len(endpoints) > 30:
            table.add_row(f"... and {len(endpoints) - 30} more")
        console.print(table)
    else:
        console.print(Panel("-", title="Endpoints", border_style="cyan"))
    console.print()

    _print_section("form")
    forms = results.get("forms", [])
    if forms:
        table = Table(title="Forms")
        table.add_column("Action")
        table.add_column("Method")
        table.add_column("Inputs")
        for form in forms:
            if isinstance(form, dict):
                table.add_row(
                    str(form.get("action", "-")),
                    str(form.get("method", "-")),
                    str(form.get("inputs", "-")),
                )
        console.print(table)
    else:
        console.print(Panel("-", title="Forms", border_style="cyan"))
    console.print()

    _print_section("comment")
    comments = results.get("comments", [])
    if comments:
        table = Table(title="Comments")
        table.add_column("Keyword")
        table.add_column("Comment")
        for item in comments[:20]:
            if isinstance(item, dict):
                table.add_row(
                    str(item.get("keyword", "-")),
                    str(item.get("comment", "-")),
                )
        console.print(table)
    else:
        console.print(Panel("-", title="Comments", border_style="cyan"))
    console.print()

    _print_section("email")
    emails = results.get("emails", [])
    if emails:
        _print_list("Emails", emails)
    else:
        console.print(Panel("-", title="Emails", border_style="cyan"))
        console.print()

    _print_section("evidence")
    evidence = results.get("evidence", [])
    if evidence:
        table = Table(title="Evidence")
        table.add_column("Source")
        table.add_column("Type")
        table.add_column("Value")
        table.add_column("Confidence")

        for ev in evidence[:30]:
            if isinstance(ev, dict):
                table.add_row(
                    str(ev.get("engine", "-")),
                    str(ev.get("type", "-")),
                    str(ev.get("value", "-")),
                    str(ev.get("confidence", 0)),
                )

        console.print(table)
    else:
        console.print(Panel("-", title="Evidence", border_style="cyan"))
    console.print()

    # =========================
    # DEEP SECTIONS
    # =========================
    if deep:
        _print_section("dns")
        _print_mapping("DNS", results.get("dns", {}))

        _print_section("tls")
        _print_mapping("TLS", results.get("tls", {}))

        _print_section("robots")
        _print_mapping("Robots", results.get("robots", {}))

        _print_section("sitemap")
        _print_list("Sitemap", results.get("sitemap", []))

        _print_section("js")
        _print_list("JavaScript", results.get("javascript", []))

        _print_section("cms")
        cms = results.get("cms") or "-"
        console.print(Panel(str(cms), title="CMS", border_style="cyan"))
        console.print()

        _print_section("wordpress")
        wordpress = results.get("wordpress") or {}
        if isinstance(wordpress, dict) and wordpress:
            table = Table(title="WordPress")
            table.add_column("Field")
            table.add_column("Value")
            for k, v in wordpress.items():
                table.add_row(str(k), str(v))
            console.print(table)
        else:
            console.print(Panel("-", title="WordPress", border_style="cyan"))
        console.print()

        _print_section("waf")
        waf = results.get("waf") or "-"
        console.print(Panel(str(waf), title="WAF", border_style="cyan"))
        console.print()

        _print_section("confidence")
        confidence = results.get("confidence", {})
        _print_mapping("Confidence", confidence)

        # adapters
        for adapter_name in ["httpx", "whatweb", "wpscan", "wafw00f", "katana", "subfinder"]:
            _print_section(adapter_name)
            adapter_data = results.get(adapter_name, {})
            if isinstance(adapter_data, dict):
                _print_mapping(adapter_name.upper(), adapter_data)
            elif isinstance(adapter_data, list):
                _print_list(adapter_name.upper(), adapter_data)
            else:
                console.print(Panel(str(adapter_data), title=adapter_name.upper(), border_style="cyan"))
                console.print()

    console.print("[bold green]✓ Scan Completed[/bold green]")