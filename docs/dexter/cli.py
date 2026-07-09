import time

import typer
from rich import box
from rich.panel import Panel

import dexter
from dexter.core.scanner import Scanner
from dexter.reports.reporter import Reporter
from dexter.ui.banner import render_banner
from dexter.ui.console import console
from dexter.ui.modules_table import modules
from dexter.ui.render import render_section, render_deep_warning
from dexter.ui.report_panel import render_scan

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="DEXTER (D3XT3COGNITION) — authorized website reconnaissance framework.",
)


def _version_string():
    return f"v{getattr(dexter, '__version__', '0.1.0')}"


def _run_scan(target, deep, show_progress=True):
    """Runs the scan, streaming each section to the terminal, and returns
    the aggregated results dict."""
    scanner = Scanner()
    results = {}
    started = time.time()
    completed = 0

    if show_progress:
        with console.status("[bold cyan]Booting reconnaissance engines...[/bold cyan]", spinner="dots") as status:
            for section, data in scanner.iter_scan(target, deep=deep):
                completed += 1
                status.stop()
                render_section(section, data)
                results[section] = data
                status.start()
                status.update(f"[bold cyan]Running module {completed + 1}...[/bold cyan]")
    else:
        for section, data in scanner.iter_scan(target, deep=deep):
            completed += 1
            results[section] = data

    elapsed = time.time() - started
    return results, completed, elapsed


@app.command()
def scan(
    target: str,
    deep: bool = typer.Option(False, "--deep", help="Run deeper reconnaissance (DNS, TLS, WAF, CMS, adapters)"),
    summary: bool = typer.Option(True, "--summary/--no-summary", help="Show the final summary panel"),
    save: bool = typer.Option(False, "--save", help="Save JSON/Markdown/Text/HTML reports after the scan"),
):
    """Scan a target and stream findings to the terminal."""
    render_banner(_version_string())
    if deep:
        render_deep_warning()

    try:
        results, completed, elapsed = _run_scan(target, deep)
    except Exception as exc:  # keep the CLI alive on unexpected failures
        console.print(Panel(f"[bold red]Scan failed:[/bold red] {exc}", border_style="red", box=box.ROUNDED))
        raise typer.Exit(code=1)

    console.print()
    modules(results)
    console.print()

    if summary:
        render_scan(target, results)

    console.print(f"[dim]Completed {completed} module(s) in {elapsed:.2f}s[/dim]")

    if save:
        directory = Reporter().save(target, results)
        console.print()
        console.print(
            Panel(
                f"[bold]JSON[/bold]  -> {directory / 'report.json'}\n"
                f"[bold]MD[/bold]    -> {directory / 'report.md'}\n"
                f"[bold]TXT[/bold]   -> {directory / 'report.txt'}\n"
                f"[bold]HTML[/bold]  -> {directory / 'report.html'}",
                title="[bold green]Reports saved[/bold green]",
                border_style="green",
                box=box.ROUNDED,
            )
        )


@app.command()
def report(
    target: str,
    deep: bool = typer.Option(False, "--deep", help="Run deeper reconnaissance before generating the report"),
    output: str = typer.Option("reports", "--output", "-o", help="Base directory to write reports into"),
):
    """Run a full scan and write JSON, Markdown, Text and HTML reports to disk."""
    render_banner(_version_string())
    if deep:
        render_deep_warning()

    try:
        results, completed, elapsed = _run_scan(target, deep)
    except Exception as exc:
        console.print(Panel(f"[bold red]Scan failed:[/bold red] {exc}", border_style="red", box=box.ROUNDED))
        raise typer.Exit(code=1)

    console.print()
    modules(results)
    console.print()
    render_scan(target, results)
    console.print(f"[dim]Completed {completed} module(s) in {elapsed:.2f}s[/dim]")

    directory = Reporter().save(target, results, base_dir=output)

    console.print()
    console.print(
        Panel(
            f"[bold]JSON[/bold]  -> {directory / 'report.json'}\n"
            f"[bold]MD[/bold]    -> {directory / 'report.md'}\n"
            f"[bold]TXT[/bold]   -> {directory / 'report.txt'}\n"
            f"[bold]HTML[/bold]  -> {directory / 'report.html'}",
            title="[bold green]Reports saved[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        )
    )


@app.command()
def version():
    """Show the DEXTER banner and version."""
    render_banner(_version_string())


if __name__ == "__main__":
    app()
