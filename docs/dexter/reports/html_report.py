from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

SECTION_TITLES = {
    "target": "Target",
    "host": "Host",
    "header": "HTTP Headers",
    "headers": "HTTP Headers",
    "cookie": "Cookies",
    "cookies": "Cookies",
    "metadata": "Metadata",
    "security_headers": "Security Headers",
    "technology": "Technologies",
    "framework": "Framework",
    "versions": "Versions",
    "version": "Versions",
    "fingerprints": "Fingerprints",
    "knowledge": "Knowledge Base Matches",
    "endpoints": "Endpoints",
    "forms": "Forms",
    "comments": "Interesting Comments",
    "emails": "Emails",
    "dns": "DNS",
    "tls": "TLS",
    "robots": "Robots.txt",
    "sitemap": "Sitemap",
    "javascript": "JavaScript Assets",
    "cms": "CMS",
    "wordpress": "WordPress",
    "waf": "WAF",
    "confidence": "Confidence Scores",
    "httpx": "httpx",
    "whatweb": "WhatWeb",
    "wpscan": "WPScan",
    "wafw00f": "WAFW00F",
    "katana": "Katana",
    "subfinder": "Subfinder",
    "evidence": "Evidence",
    "adapters": "External Adapters",
}

SKIP_KEYS = {"target", "host"}


def _title(key):
    return SECTION_TITLES.get(key, str(key).replace("_", " ").title())


def _normalize_section(key, value):
    title = _title(key)

    if isinstance(value, dict) and set(value.keys()) == {"error"}:
        return {"title": title, "kind": "error", "error": str(value["error"])}

    if isinstance(value, dict):
        rows = list(value.items())
        return {"title": title, "kind": "mapping", "rows": rows}

    if isinstance(value, list):
        if value and all(isinstance(v, dict) for v in value):
            columns = []
            for item in value:
                for col in item.keys():
                    if col not in columns:
                        columns.append(col)
            columns = columns[:6]
            return {"title": title, "kind": "table", "columns": columns, "rows": value}
        return {"title": title, "kind": "list", "rows": [str(v) for v in value]}

    return {"title": title, "kind": "text", "text": "" if value is None else str(value)}


class HTMLReport:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(["html"]),
        )

    def _render(self, target, data):
        sections = [
            _normalize_section(key, value)
            for key, value in data.items()
            if key not in SKIP_KEYS
        ]

        template = self.env.get_template("report.html")
        return template.render(
            target=target,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            deep=bool(data.get("dns") or data.get("tls") or data.get("waf")),
            sections=sections,
        )

    def save(self, directory, data):
        target = data.get("target") or data.get("host") or "target"
        html = self._render(target, data)

        with open(directory / "report.html", "w", encoding="utf-8") as f:
            f.write(html)
