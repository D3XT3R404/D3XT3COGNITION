from dexter.ui.banner import banner

from dexter.ui.modules_table import modules

from dexter.ui.technology_table import technologies

from dexter.ui.report_panel import reports


def render(

        results

):

    banner()

    modules(

        results

    )

    technologies(

        results.get(

            "technologies",

            []

        )

    )

    reports(

        results[

            "target"

        ]

    )