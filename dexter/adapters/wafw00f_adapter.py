import re
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class Wafw00fAdapter(BaseAdapter):
    binary = "wafw00f"

    def execute(self, target, results=None):
        url = self.normalize_target(target)

        output = {
            "source": "wafw00f",
            "detected": False,
            "waf": None,
            "error": None,
        }

        if not self.available():
            output["error"] = "wafw00f binary not found"
            return output

        try:
            cmd = [
                self.binary,
                url,
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            raw = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()

            if proc.returncode != 0 and not raw:
                output["error"] = f"wafw00f exited with code {proc.returncode}"
                return output

            waf = None

            m = re.search(r"is behind\s+(?P<waf>[^.\n]+)", raw, re.I)
            if m:
                waf = m.group("waf").strip()

            if not waf:
                m = re.search(r"behind\s+(?P<waf>[^.\n]+)", raw, re.I)
                if m:
                    waf = m.group("waf").strip()

            if not waf and "no waf detected" in raw.lower():
                waf = None

            output["waf"] = waf
            output["detected"] = bool(waf)

        except Exception as e:
            output["error"] = str(e)

        return output
