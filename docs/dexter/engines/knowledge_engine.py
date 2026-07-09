import re
from pathlib import Path
import yaml

from dexter.core.base_engine import BaseEngine


class KnowledgeEngine(BaseEngine):
    def __init__(self):
        self._index = None

    def _index_files(self):
        if self._index is not None:
            return self._index

        base = Path(__file__).resolve().parents[1] / "knowledge" / "software"
        index = {}
        for path in base.rglob("*.yaml"):
            index[path.stem.lower()] = path
        self._index = index
        return index

    def _canonical(self, name):
        if not name:
            return None

        n = re.sub(r"[^a-z0-9]+", "", str(name).lower())
        aliases = {
            "apachehttpserver": "apache",
            "apache": "apache",
            "nginx": "nginx",
            "php": "php",
            "wordpress": "wordpress",
            "laravel": "laravel",
            "jquery": "jquery",
            "bootstrap": "bootstrap",
            "nextjs": "nextjs",
            "nextjsdata": "nextjs",
            "openssh": "openssh",
            "vsftpd": "vsftpd",
            "cloudflare": "cloudflare",
        }
        return aliases.get(n, n)

    def _parts(self, version):
        nums = [int(x) for x in re.findall(r"\d+", str(version))]
        return tuple(nums[:4] or [0])

    def _compare(self, a, b):
        pa = self._parts(a)
        pb = self._parts(b)
        length = max(len(pa), len(pb))
        pa = pa + (0,) * (length - len(pa))
        pb = pb + (0,) * (length - len(pb))
        return (pa > pb) - (pa < pb)

    def _match(self, spec, version):
        if not spec or not version:
            return False

        spec = str(spec).strip()
        version = str(version).strip()

        if spec == version:
            return True

        if " - " in spec:
            low, high = [x.strip() for x in spec.split(" - ", 1)]
            return self._compare(version, low) >= 0 and self._compare(version, high) <= 0

        if spec.startswith("<="):
            return self._compare(version, spec[2:].strip()) <= 0
        if spec.startswith(">="):
            return self._compare(version, spec[2:].strip()) >= 0
        if spec.startswith("<"):
            return self._compare(version, spec[1:].strip()) < 0
        if spec.startswith(">"):
            return self._compare(version, spec[1:].strip()) > 0

        if spec.endswith(".x"):
            return version.startswith(spec[:-2] + ".") or version.startswith(spec[:-2])

        return False

    def _pick_entry(self, db, version):
        versions_db = db.get("versions", {})
        if not isinstance(versions_db, dict):
            versions_db = {}

        if version:
            for spec, entry in versions_db.items():
                if self._match(spec, version):
                    if isinstance(entry, dict):
                        return spec, entry

        return None, {
            "status": db.get("status", "unknown"),
            "severity": db.get("severity", "info"),
            "cves": [],
            "description": db.get("description"),
            "notes": db.get("notes", []),
            "references": db.get("references", []),
            "attack_surface": db.get("attack_surface", []),
        }

    def run(self, target):
        results = getattr(target, "results", {}) if not isinstance(target, dict) else target
        index = self._index_files()
        output = []
        seen = set()

        candidates = []

        versions = results.get("versions", {})
        if isinstance(versions, dict):
            for name, version in versions.items():
                candidates.append((name, version))

        framework = results.get("framework")
        if framework:
            candidates.append((framework, versions.get(framework)))

        cms = results.get("cms")
        if cms:
            candidates.append((cms, versions.get(cms)))

        wordpress = results.get("wordpress", {})
        if isinstance(wordpress, dict) and wordpress.get("detected"):
            candidates.append(("WordPress", wordpress.get("version")))

        technology = results.get("technology", [])
        if isinstance(technology, list):
            for tech in technology:
                candidates.append((tech, versions.get(tech)))

        httpx = results.get("httpx", {})
        if isinstance(httpx, dict):
            for item in httpx.get("items", []):
                if not isinstance(item, dict):
                    continue
                for tech in item.get("tech", []):
                    if ":" in str(tech) and not str(tech).startswith("http"):
                        name, ver = str(tech).split(":", 1)
                    else:
                        name, ver = str(tech), None
                    candidates.append((name, ver))

                webserver = item.get("webserver")
                if webserver:
                    candidates.append((webserver, None))

        whatweb = results.get("whatweb", {})
        if isinstance(whatweb, dict):
            for item in whatweb.get("detected", []):
                if not isinstance(item, dict):
                    continue
                candidates.append((item.get("name"), item.get("version")))

        for name, version in candidates:
            stem = self._canonical(name)
            if not stem or stem in seen:
                continue
            seen.add(stem)

            path = index.get(stem)
            if not path:
                continue

            try:
                db = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except Exception:
                continue

            matched_spec, matched_entry = self._pick_entry(db, version)

            knowledge = {
                "name": db.get("name", name),
                "versions": matched_entry,
                "attack_surface": db.get("attack_surface", []),
                "references": db.get("references", []),
                "notes": db.get("notes", []),
            }

            output.append(
                {
                    "software": db.get("name", name),
                    "version": version,
                    "matched_spec": matched_spec,
                    "knowledge": knowledge,
                }
            )

        results["knowledge"] = output
        return output