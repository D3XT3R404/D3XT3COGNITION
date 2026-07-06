import json
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class HttpxAdapter(BaseAdapter):
    binary = "httpx"

    def execute(self, target, results=None):
        output = {
            "source": "httpx",
            "raw": "",
            "parsed": [],
            "error": None,
        }

        if not self.available():
            output["error"] = "httpx binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "-json",
                "-title",
                "-tech-detect",
                "-status-code",
                "-follow-redirects",
                "-silent",
                "-u",
                target,
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
            )

            raw = (proc.stdout or "").strip()
            output["raw"] = raw

            if proc.returncode != 0 and not raw:
                output["error"] = f"httpx exited with code {proc.returncode}"
                return output

            parsed = []
            for line in raw.splitlines():
                try:
                    item = json.loads(line)
                    parsed.append(item)
                except Exception:
                    continue

            output["parsed"] = parsed

        except Exception as e:
            output["error"] = str(e)

        return output