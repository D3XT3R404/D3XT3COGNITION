import os
import yaml

from dexter.core.base_engine import BaseEngine


class KnowledgeEngine(BaseEngine):

    name = "knowledge"

    def run(self, context):

        base = os.path.join(

            os.path.dirname(__file__),

            "..",

            "knowledge",

            "software"

        )

        results = []

        versions = context.results.get(

            "versions",

            {}

        )

        for software in versions:

            file = os.path.join(

                base,

                software.lower() + ".yaml"

            )

            if not os.path.exists(file):

                continue

            with open(

                file,

                encoding="utf-8"

            ) as f:

                db = yaml.safe_load(f)

            results.append(

                {

                    "software": software,

                    "version": versions[software],

                    "knowledge": db

                }

            )

        return results