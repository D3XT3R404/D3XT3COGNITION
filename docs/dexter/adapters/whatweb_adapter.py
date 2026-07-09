import re
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class WhatWebAdapter(BaseAdapter):
    binary = "whatweb"

    def execute(self, target, results=None):
        url = self.normalize_target(target)

        output = {
            "source": "whatweb",
            "detected": [],
            "error": None,
        }

        if not self.available():
            output["error"] = "whatweb binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "--color=never",
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
                output["error"] = f"whatweb exited with code {proc.returncode}"
                return output

            detected = []
            for line in raw.splitlines():
                if "[" not in line and "," not in line:
                    continue

                for chunk in re.split(r",\s*", line):
                    chunk = chunk.strip()
                    if not chunk:
                        continue
                    if chunk.lower().startswith(("whatweb", "target", "http://", "https://")):
                        continue

                    m = re.match(
                        r"^(?P<name>[A-Za-z0-9_.+\- ]+?)(?:\[(?P<version>[^\]]+)\])?$",
                        chunk,
                    )
                    if not m:
                        continue

                    name = m.group("name").strip()
                    version = (m.group("version") or "").strip() or None
                    if not name:
                        continue

                    detected.append(
                        {
                            "name": name,
                            "version": version,
                            "confidence": 70,
                            "source": "whatweb",
                        }
                    )

            output["detected"] = detected

        except Exception as e:
            output["error"] = str(e)

        return output
