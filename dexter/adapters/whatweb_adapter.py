import re
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class WhatWebAdapter(BaseAdapter):
    binary = "whatweb"

    def execute(self, target, results=None):
        output = {
            "source": "whatweb",
            "detected": [],
            "raw": "",
            "error": None,
        }

        if not self.available():
            output["error"] = "whatweb binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "--color=never",
                "--no-errors",
                target,
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
            output["raw"] = raw.strip()

            if proc.returncode != 0 and not raw.strip():
                output["error"] = f"whatweb exited with code {proc.returncode}"
                return output

            detected = []

            # WhatWeb output biasanya seperti:
            # Apache[2.4.63], PHP[8.3.29], WordPress, jQuery
            tokens = re.findall(r"([A-Za-z0-9_.+-]+)(?:\[(.*?)\])?", raw)

            for name, version in tokens:
                name = name.strip()
                version = version.strip()

                if not name:
                    continue

                if name.lower() in {"whatweb", "target"}:
                    continue

                item = {
                    "name": name,
                    "version": version or None,
                    "confidence": 70,
                    "source": "whatweb",
                }
                detected.append(item)

            output["detected"] = detected

        except Exception as e:
            output["error"] = str(e)

        return output