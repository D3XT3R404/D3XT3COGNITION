import os
import yaml

from dexter.core.base_engine import BaseEngine


class KnowledgeEngine(BaseEngine):

    def _load_db(self, software):
        base_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "knowledge",
            "software",
        )

        path = os.path.join(base_dir, f"{software.lower()}.yaml")
        if not os.path.exists(path):
            return None

        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def run(self, target):
        results = {}

        try:
            if isinstance(target, dict):
                versions = target.get("versions", {})
            else:
                versions = {}
        except Exception:
            versions = {}

        if not isinstance(versions, dict):
            return []

        output = []

        for software, version in versions.items():
            db = self._load_db(software)
            if not db:
                continue

            output.append({
                "software": software,
                "version": version,
                "knowledge": db,
            })

        return output