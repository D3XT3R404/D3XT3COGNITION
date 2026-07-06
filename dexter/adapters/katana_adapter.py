import json
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class KatanaAdapter(BaseAdapter):
    binary = "katana"

    def execute(self, target, results=None):
        output = {
            "source": "katana",
            "urls": [],
            "raw": "",
            "error": None,
        }

        if not self.available():
            output["error"] = "katana binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "-u",
                target,
                "-json",
                "-silent",
                "-d",
                "3",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            raw = (proc.stdout or "").strip()
            output["raw"] = raw

            urls = []
            for line in raw.splitlines():
                try:
                    item = json.loads(line)
                    url = item.get("url") or item.get("request")
                    if url:
                        urls.append(url)
                except Exception:
                    continue

            output["urls"] = sorted(set(urls))

        except Exception as e:
            output["error"] = str(e)

        return output