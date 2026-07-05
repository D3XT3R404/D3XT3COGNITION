import typer

from dexter.core.scanner import Scanner
from dexter.ui.report_panel import render_scan

app = typer.Typer()


@app.command()
def scan(
    target: str,
    deep: bool = False,
):

    scanner = Scanner()

    results = scanner.scan(target, deep)

    render_scan(target, results)


@app.command()
def version():

    print("DEXTER v0.1")


@app.command()
def report(
    target: str,
):

    print(f"Generating report for {target}...")


if __name__ == "__main__":
    app()