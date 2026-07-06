from dexter.core.base_engine import BaseEngine


class ConfidenceEngine(BaseEngine):

    def run(self, target):
        scores = {}

        if isinstance(target, dict):
            scores["raw"] = 0
        return scores