from collections import defaultdict

from dexter.core.base_engine import BaseEngine


class ConfidenceEngine(BaseEngine):
    def _bump(self, scores, key, amount):
        scores[key] = min(100, scores.get(key, 0) + amount)

    def run(self, target):
        results = getattr(target, "results", {}) if not isinstance(target, dict) else target
        scores = {}

        techs = results.get("technology", [])
        for tech in techs:
            if tech:
                self._bump(scores, str(tech).lower(), 55)

        evidence = results.get("evidence", [])
        for ev in evidence:
            if not isinstance(ev, dict):
                continue
            value = str(ev.get("value", "")).lower()
            conf = int(ev.get("confidence", 0) or 0)

            if "wordpress" in value:
                self._bump(scores, "wordpress", max(conf, 35))
            if "laravel" in value:
                self._bump(scores, "laravel", max(conf, 35))
            if "apache" in value:
                self._bump(scores, "apache", max(conf, 35))
            if "php" in value:
                self._bump(scores, "php", max(conf, 35))
            if "jquery" in value:
                self._bump(scores, "jquery", max(conf, 25))

        wordpress = results.get("wordpress", {})
        if isinstance(wordpress, dict) and wordpress.get("detected"):
            self._bump(scores, "wordpress", 95)

        cms = results.get("cms")
        if cms:
            self._bump(scores, str(cms).lower(), 90)

        framework = results.get("framework")
        if framework:
            self._bump(scores, str(framework).lower(), 85)

        w = results.get("waf", {})
        if isinstance(w, dict) and w.get("detected") and w.get("name"):
            self._bump(scores, f"waf:{str(w['name']).lower()}", w.get("confidence", 60))

        scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        results["confidence"] = scores
        return scores