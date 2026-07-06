import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class Wafw00fAdapter(BaseAdapter):
    binary = "wafw00f"

    def execute(self, target, results=None):
        output = {
            "source": "wafw00f",
            "waf": None,
            "raw": "",
            "error": None,
        }

        if not self.available():
            output["error"] = "wafw00f binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "--no-color",
                target,
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
            )

            raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
            output["raw"] = raw.strip()

            waf = None
            for line in raw.splitlines():
                low = line.lower()
                if "waf" in low and "is" in low:
                    waf = line.strip()

            output["waf"] = waf

        except Exception as e:
            output["error"] = str(e)

        return output