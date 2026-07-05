class ConfidenceEngine:

    def calculate(

            self,

            score

    ):

        if score >= 90:

            return "very_high"

        if score >= 70:

            return "high"

        if score >= 50:

            return "medium"

        return "low"