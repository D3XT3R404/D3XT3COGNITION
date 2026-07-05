class EngineRegistry:

    def __init__(self):

        self.engines = []

    def register(
            self,
            engine
    ):

        self.engines.append(

            engine

        )

    def run(

            self,

            target

    ):

        results = {}

        for engine in self.engines:

            results[

                engine.name

            ] = engine.run(

                target

            )

        return results