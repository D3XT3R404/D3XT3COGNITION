import yaml

from pathlib import Path


class KnowledgeEngine:

    name = "knowledge"

    def __init__(self):

        self.db_path = Path(

            "dexter/knowledge"

        )

        self.cache = {}

        self._load_db()


    # -------------------------

    def _load_db(self):

        for file in self.db_path.rglob("*.yaml"):

            with open(file, "r", encoding="utf-8") as f:

                data = yaml.safe_load(f)

                if data:

                    self.cache[data["name"].lower()] = data


    # -------------------------

    def _match_version(self, version, rule_version):

        if not version or not rule_version:

            return False

        if rule_version.startswith("<"):

            return version < rule_version[1:]

        if "-" in rule_version:

            start, end = rule_version.split("-")

            return start.strip() <= version <= end.strip()

        return version == rule_version


    # -------------------------

    def run(self, data):

        techs = data.get("technologies", [])

        results = []

        for tech in techs:

            name = tech.get("name", "").lower()

            version = tech.get("version", "")

            if name not in self.cache:

                continue

            db = self.cache[name]

            versions = db.get("versions", {})

            for v_rule, v_data in versions.items():

                if self._match_version(version, v_rule):

                    results.append({

                        "name": tech.get("name"),

                        "version": version,

                        "severity": v_data.get("severity", "unknown"),

                        "cves": v_data.get("cves", []),

                        "description": v_data.get("description", ""),

                        "notes": v_data.get("notes", []),

                        "confidence": 90

                    })

                    break

        return results