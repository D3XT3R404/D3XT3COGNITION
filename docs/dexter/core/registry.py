class EngineRegistry:
    def __init__(self):
        self.engines = []

    def register(self, engine):
        self.engines.append(engine)

    def run(self, context):
        results = {}

        for engine in self.engines:
            try:
                data = engine.run(context)
                results[engine.name] = data
                context.results[engine.name] = data
            except Exception as e:
                error_data = {"error": str(e)}
                results[engine.name] = error_data
                context.results[engine.name] = error_data

        return results