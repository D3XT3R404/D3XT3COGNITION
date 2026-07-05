class HTMLReport:

    def save(

            self,

            directory,

            data

    ):

        html = """

<html>

<head>

<title>

DEXTER Report

</title>

</head>

<body>

<h1>

DEXTER Report

</h1>

"""

        for k, v in data.items():

            html += (

                f"<h2>{k}</h2>"

            )

            html += (

                f"<pre>{v}</pre>"

            )

        html += (

            "</body></html>"

        )

        with open(

                directory /

                "report.html",

                "w",

                encoding="utf-8"

        ) as f:

            f.write(

                html

            )