import re
from datetime import datetime
from pathlib import Path

from dexter.reports.json_report import JSONReport
from dexter.reports.markdown_report import MarkdownReport
from dexter.reports.text_report import TextReport
from dexter.reports.html_report import HTMLReport


def _safe_name(target):
    """Turn a target/URL into a filesystem-friendly directory name."""
    name = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", str(target or "").strip())
    name = name.rstrip("/")
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    return name.strip("_") or "target"


class Reporter:

    def save(self, target, data, base_dir="reports"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        directory = Path(base_dir) / _safe_name(target) / timestamp

        directory.mkdir(

            parents=True,

            exist_ok=True

        )

        JSONReport().save(

            directory,

            data

        )

        MarkdownReport().save(

            directory,

            data

        )

        TextReport().save(

            directory,

            data

        )

        HTMLReport().save(

            directory,

            data

        )

        return directory