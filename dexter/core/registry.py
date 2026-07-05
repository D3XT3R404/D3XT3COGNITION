from rich.console import Console

console = Console()


class EngineRegistry:

    def __init__(self):

        self.engines = []

    def register(self, engine):

        self.engines.append(engine)

    def run(self, context):

        results = {}

        for engine in self.engines:

            console.print(
                f"[cyan][*][/cyan] {engine.name}"
            )

            try:

                data = engine.run(context)

                results[engine.name] = data

                context.results[engine.name] = data

            except Exception as e:

                console.print(
                    f"[red][ERROR][/red] {engine.name}: {e}"
                )

                context.errors.append(

                    str(e)

                )

        return results