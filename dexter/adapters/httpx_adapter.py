import json
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class HttpxAdapter(BaseAdapter):
    binary = "httpx"

    def execute(self, target, results=None):
        url = self.normalize_target(target)

        output = {
            "source": "httpx",
            "summary": {},
            "items": [],
            "error": None,
        }

        if not self.available():
            output["error"] = "httpx binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "-u",
                url,
                "-j",
                "-title",
                "-td",
                "-sc",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
            )

            raw = (proc.stdout or "").strip()
            if proc.returncode != 0 and not raw:
                output["error"] = f"httpx exited with code {proc.returncode}"
                return output

            items = []
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    items.append(item)
                except Exception:
                    continue

            output["items"] = items

            if items:
                item = items[0]
                output["summary"] = {
                    "url": item.get("url", url),
                    "title": item.get("title"),
                    "status_code": item.get("status_code"),
                    "webserver": item.get("webserver"),
                    "host_ip": item.get("host_ip"),
                    "scheme": item.get("scheme"),
                    "content_type": item.get("content_type"),
                    "tech": item.get("tech", []),
                    "cpe": item.get("cpe", []),
                    "jarm": item.get("jarm"),
                    "cdn": item.get("cdn"),
                }

        except Exception as e:
            output["error"] = str(e)

        return output