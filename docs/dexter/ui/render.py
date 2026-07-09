from rich import box
from rich.panel import Panel
from rich.table import Table

from dexter.ui.console import console

LIMITS = {
    "metadata": 16,
    "httpx_items": 8,
    "whatweb": 16,
    "katana": 24,
    "subfinder": 24,
    "wpscan": 16,
    "wordpress": 16,
    "tls": 16,
    "default_list": 24,
    "default_dict": 16,
}

SECTION_TITLES = {
    "header": "HTTP Headers",
    "cookie": "Cookies",
    "metadata": "Metadata",
    "security_headers": "Security Headers",
    "technology": "Technologies",
    "versions": "Versions",
    "version": "Versions",
    "fingerprints": "Fingerprints",
    "knowledge": "Knowledge",
    "endpoints": "Endpoints",
    "forms": "Forms",
    "comments": "Interesting Comments",
    "emails": "Emails",
    "dns": "DNS",
    "tls": "TLS",
    "robots": "Robots",
    "sitemap": "Sitemap",
    "javascript": "JavaScript Assets",
    "cms": "CMS",
    "wordpress": "WordPress",
    "waf": "WAF",
    "confidence": "Confidence",
    "httpx": "httpx",
    "whatweb": "WhatWeb",
    "wpscan": "WPScan",
    "wafw00f": "WAFW00F",
    "katana": "Katana",
    "subfinder": "Subfinder",
    "evidence": "Evidence",
}


def render_deep_warning():
    console.print(
        Panel(
            "[bold yellow]Deep scan enabled[/bold yellow]\n"
            "External adapters and heavier checks may take longer. "
            "Missing tools will be skipped gracefully.",
            border_style="yellow",
            box=box.ROUNDED,
        )
    )
    console.print()


def _title(section):
    return SECTION_TITLES.get(section, section.replace("_", " ").title())


def _short_value(value, limit=140):
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple, set)):
        values = list(value)
        if not values:
            return "-"
        preview = ", ".join(_short_value(v, 45) for v in values[:4])
        if len(values) > 4:
            preview += f" ... (+{len(values) - 4})"
        return preview
    if isinstance(value, dict):
        if not value:
            return "-"
        preview = ", ".join(f"{k}={_short_value(v, 35)}" for k, v in list(value.items())[:4])
        if len(value) > 4:
            preview += f" ... (+{len(value) - 4})"
        return preview

    text = str(value).replace("\n", " ").strip()
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text or "-"


def _is_missing_adapter(data):
    if not isinstance(data, dict):
        return False
    error = str(data.get("error") or "").lower()
    return "not found" in error or "binary not found" in error


def _empty_panel(title, note="No data found."):
    return Panel(f"[dim]{note}[/dim]", title=title, border_style="dim", box=box.ROUNDED)


def _summary_note(shown, total):
    if total > shown:
        return f"showing {shown} of {total}"
    return f"{total} item(s)"


def _mapping_table(title, data, limit=None):
    limit = limit or LIMITS["default_dict"]
    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    if isinstance(data, dict) and data:
        items = list(data.items())
        for key, value in items[:limit]:
            table.add_row(str(key), _short_value(value))
        if len(items) > limit:
            table.caption = _summary_note(limit, len(items))
    else:
        table.add_row("-", "-")

    return table


def _list_table(title, items, limit=None, column="Item"):
    limit = limit or LIMITS["default_list"]
    table = Table(title=title, box=box.SIMPLE)
    table.add_column(column, style="green")

    if isinstance(items, (list, tuple, set)) and items:
        values = list(items)
        for item in values[:limit]:
            table.add_row(_short_value(item, 180))
        if len(values) > limit:
            table.caption = _summary_note(limit, len(values))
    else:
        table.add_row("-")

    return table


def _render_status_panel(title, data):
    if isinstance(data, dict) and data.get("error"):
        style = "dim" if _is_missing_adapter(data) else "yellow"
        console.print(
            Panel(
                _short_value(data.get("error"), 220),
                title=title,
                border_style=style,
                box=box.ROUNDED,
            )
        )
        return True
    return False


def _render_metadata(data):
    title = _title("metadata")
    if not isinstance(data, dict) or not data:
        console.print(_empty_panel(title))
        return

    overview = {}
    if data.get("title"):
        overview["title"] = data.get("title")

    meta = data.get("meta", {})
    if isinstance(meta, dict):
        overview["meta_fields"] = len(meta)

    if overview:
        console.print(_mapping_table("Metadata Overview", overview, limit=8))
    if isinstance(meta, dict) and meta:
        console.print(_mapping_table("Meta Fields", meta, limit=LIMITS["metadata"]))


def _render_httpx(data):
    title = _title("httpx")
    if _render_status_panel(title, data):
        return
    if not isinstance(data, dict) or not data:
        console.print(_empty_panel(title))
        return

    summary = data.get("summary", {})
    if isinstance(summary, dict) and summary:
        console.print(_mapping_table("httpx Summary", summary, limit=16))

    items = data.get("items", [])
    if isinstance(items, list) and items:
        table = Table(title="httpx Items", box=box.SIMPLE)
        table.add_column("URL", style="green")
        table.add_column("Status", justify="right")
        table.add_column("Title", style="cyan")
        table.add_column("Tech", style="magenta")
        table.add_column("Server")
        for item in items[: LIMITS["httpx_items"]]:
            if not isinstance(item, dict):
                continue
            table.add_row(
                _short_value(item.get("url"), 70),
                _short_value(item.get("status_code"), 8),
                _short_value(item.get("title"), 50),
                _short_value(item.get("tech"), 60),
                _short_value(item.get("webserver"), 35),
            )
        if len(items) > LIMITS["httpx_items"]:
            table.caption = _summary_note(LIMITS["httpx_items"], len(items))
        console.print(table)


def _render_whatweb(data):
    title = _title("whatweb")
    if _render_status_panel(title, data):
        return
    detected = data.get("detected", []) if isinstance(data, dict) else []
    if not detected:
        console.print(_empty_panel(title))
        return

    table = Table(title="WhatWeb Detected", box=box.SIMPLE)
    table.add_column("Name", style="green")
    table.add_column("Version", style="cyan")
    table.add_column("Confidence", justify="right")
    for item in detected[: LIMITS["whatweb"]]:
        if isinstance(item, dict):
            table.add_row(
                _short_value(item.get("name"), 50),
                _short_value(item.get("version"), 25),
                _short_value(item.get("confidence"), 10),
            )
        else:
            table.add_row(_short_value(item, 80), "-", "-")
    if len(detected) > LIMITS["whatweb"]:
        table.caption = _summary_note(LIMITS["whatweb"], len(detected))
    console.print(table)


def _render_katana(data):
    title = _title("katana")
    if _render_status_panel(title, data):
        return
    urls = data.get("urls", []) if isinstance(data, dict) else []
    if urls:
        console.print(_list_table("Katana URLs", urls, limit=LIMITS["katana"], column="URL"))
    else:
        console.print(_empty_panel(title, "No crawled URLs found."))


def _render_subfinder(data):
    title = _title("subfinder")
    if _render_status_panel(title, data):
        return
    subdomains = data.get("subdomains", []) if isinstance(data, dict) else []
    if subdomains:
        console.print(
            _list_table(
                "Subfinder Subdomains",
                subdomains,
                limit=LIMITS["subfinder"],
                column="Subdomain",
            )
        )
    else:
        console.print(_empty_panel(title, "No subdomains found."))


def _render_wpscan(data):
    title = _title("wpscan")
    if _render_status_panel(title, data):
        return
    if not isinstance(data, dict):
        console.print(_empty_panel(title))
        return

    wordpress = data.get("wordpress", {})
    if not isinstance(wordpress, dict) or not wordpress:
        console.print(_empty_panel(title))
        return

    summary_keys = ["detected", "version", "theme", "api_token_used"]
    summary = {key: wordpress.get(key) for key in summary_keys}
    console.print(_mapping_table("WPScan Summary", summary, limit=8))

    for key, label in (
        ("plugins", "WPScan Plugins"),
        ("themes", "WPScan Themes"),
        ("users", "WPScan Users"),
        ("interesting_findings", "WPScan Findings"),
    ):
        values = wordpress.get(key, [])
        if values:
            console.print(_list_table(label, values, limit=LIMITS["wpscan"]))


def _render_wordpress(data):
    title = _title("wordpress")
    if not isinstance(data, dict) or not data:
        console.print(_empty_panel(title))
        return

    summary = {
        "detected": data.get("detected"),
        "version": data.get("version"),
        "theme": data.get("theme"),
        "generator": data.get("generator"),
        "rest_api": data.get("rest_api"),
        "xmlrpc": data.get("xmlrpc"),
        "readme": data.get("readme"),
        "license": data.get("license"),
        "wp_cron": data.get("wp_cron"),
    }
    console.print(_mapping_table("WordPress Summary", summary, limit=12))

    plugins = data.get("plugins", [])
    if plugins:
        console.print(_list_table("WordPress Plugins", plugins, limit=LIMITS["wordpress"]))


def _render_tls(data):
    title = _title("tls")
    if not isinstance(data, dict) or not data:
        console.print(_empty_panel(title))
        return
    console.print(_mapping_table("TLS Summary", data, limit=LIMITS["tls"]))


def _render_evidence(data):
    title = _title("evidence")
    if not isinstance(data, list) or not data:
        console.print(_empty_panel(title))
        return

    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Source", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Value", style="green")
    table.add_column("Confidence", justify="right")
    for ev in data[: LIMITS["default_list"]]:
        if isinstance(ev, dict):
            table.add_row(
                _short_value(ev.get("engine"), 20),
                _short_value(ev.get("type"), 20),
                _short_value(ev.get("value"), 90),
                _short_value(ev.get("confidence"), 10),
            )
        else:
            table.add_row("-", "-", _short_value(ev, 90), "-")
    if len(data) > LIMITS["default_list"]:
        table.caption = _summary_note(LIMITS["default_list"], len(data))
    console.print(table)


def _render_knowledge(data):
    title = _title("knowledge")
    if not isinstance(data, list) or not data:
        console.print(_empty_panel(title))
        return

    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Software", style="green")
    table.add_column("Version", style="cyan")
    table.add_column("Matched Spec", style="magenta")
    for item in data[: LIMITS["default_list"]]:
        if isinstance(item, dict):
            table.add_row(
                _short_value(item.get("software"), 40),
                _short_value(item.get("version"), 20),
                _short_value(item.get("matched_spec"), 70),
            )
        else:
            table.add_row(_short_value(item, 40), "-", "-")
    if len(data) > LIMITS["default_list"]:
        table.caption = _summary_note(LIMITS["default_list"], len(data))
    console.print(table)


def render_section(section, data):
    title = _title(section)
    console.print(f"[bold cyan]>[/bold cyan] [bold]{title}[/bold]")

    if section == "metadata":
        _render_metadata(data)
    elif section == "httpx":
        _render_httpx(data)
    elif section == "whatweb":
        _render_whatweb(data)
    elif section == "katana":
        _render_katana(data)
    elif section == "subfinder":
        _render_subfinder(data)
    elif section == "wpscan":
        _render_wpscan(data)
    elif section == "wordpress":
        _render_wordpress(data)
    elif section == "tls":
        _render_tls(data)
    elif section == "knowledge":
        _render_knowledge(data)
    elif section == "evidence":
        _render_evidence(data)
    elif isinstance(data, dict):
        if _render_status_panel(title, data):
            pass
        else:
            console.print(_mapping_table(title, data, limit=LIMITS["default_dict"]))
    elif isinstance(data, list):
        console.print(_list_table(title, data, limit=LIMITS["default_list"]))
    else:
        console.print(Panel(_short_value(data), title=title, border_style="cyan", box=box.ROUNDED))

    console.print()
