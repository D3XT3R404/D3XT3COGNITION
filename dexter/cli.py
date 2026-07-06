import typer

from dexter.core.scanner import Scanner
from dexter.ui.banner import render_banner
from dexter.ui.render import render_scan

app = typer.Typer(add_completion=False)


@app.command()
def scan(
    target: str,
    deep: bool = typer.Option(False, "--deep", help="Run deeper reconnaissance"),
):

    scanner = Scanner()

    results = scanner.scan(target, deep=deep)

    render_scan(target, results, deep=deep)


@app.command()
def version():

    render_banner("v0.1")


@app.command()
def report(
    target: str,
):

    print(f"Generating report for {target}...")


if __name__ == "__main__":
    app()