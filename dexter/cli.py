import typer

from dexter.core.scanner import Scanner


app = typer.Typer()


@app.command()

def scan(

        target: str,

        deep: bool = False

):

    scanner = Scanner()

    results = scanner.scan(target, deep)

    print(results)


@app.command()

def version():

    print("DEXTER v0.1")


@app.command()

def report(

        target: str

):

    print(f"Generating report for {target}...")


if __name__ == "__main__":

    app()