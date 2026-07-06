import typer

from dexter.core.scanner import Scanner
from dexter.ui.banner import render_banner
from dexter.ui.render import render_section, render_deep_warning

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def scan(
    target: str,
    deep: bool = typer.Option(False, "--deep", help="Run deeper reconnaissance"),
):
    scanner = Scanner()

    render_banner("v0.1")
    if deep:
        render_deep_warning()

    for section, data in scanner.iter_scan(target, deep=deep):
        render_section(section, data)


@app.command()
def version():
    render_banner("v0.1")


@app.command()
def report(target: str):
    print(f"Generating report for {target}...")


if __name__ == "__main__":
    app()