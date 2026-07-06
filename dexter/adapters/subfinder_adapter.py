import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class SubfinderAdapter(BaseAdapter):
    binary = "subfinder"

    def execute(self, target, results=None):
        host = self.host_only(target)

        output = {
            "source": "subfinder",
            "subdomains": [],
            "count": 0,
            "error": None,
        }

        if not self.available():
            output["error"] = "subfinder binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "-d",
                host,
                "-all",
                "-silent",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            raw = (proc.stdout or "").strip()
            if proc.returncode != 0 and not raw:
                output["error"] = f"subfinder exited with code {proc.returncode}"
                return output

            subs = []
            for line in raw.splitlines():
                line = line.strip()
                if line:
                    subs.append(line)

            subs = sorted(set(subs))
            output["subdomains"] = subs
            output["count"] = len(subs)

        except Exception as e:
            output["error"] = str(e)

        return output