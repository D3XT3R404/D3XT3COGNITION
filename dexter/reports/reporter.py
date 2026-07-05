from pathlib import Path

from dexter.reports.json_report import JSONReport
from dexter.reports.markdown_report import MarkdownReport
from dexter.reports.text_report import TextReport
from dexter.reports.html_report import HTMLReport


class Reporter:

    def save(

            self,

            target,

            data

    ):

        directory = Path(

            "reports"

        ) / target

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