import json
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class KatanaAdapter(BaseAdapter):
    binary = "katana"

    def execute(self, target, results=None):
        url = self.normalize_target(target)

        output = {
            "source": "katana",
            "urls": [],
            "count": 0,
            "error": None,
        }

        if not self.available():
            output["error"] = "katana binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "-u",
                url,
                "-jsonl",
                "-nc",
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
            if proc.returncode != 0 and not raw:
                output["error"] = f"katana exited with code {proc.returncode}"
                return output

            urls = []
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue

                endpoint = None
                if isinstance(item, dict):
                    endpoint = item.get("url")

                    req = item.get("request", {})
                    if isinstance(req, dict):
                        endpoint = endpoint or req.get("endpoint") or req.get("url")

                    resp = item.get("response", {})
                    if isinstance(resp, dict):
                        endpoint = endpoint or resp.get("url")

                if endpoint:
                    urls.append(endpoint)

            urls = sorted(set(urls))
            output["urls"] = urls
            output["count"] = len(urls)

        except Exception as e:
            output["error"] = str(e)

        return output