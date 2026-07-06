import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class SubfinderAdapter(BaseAdapter):
    binary = "subfinder"

    def execute(self, target, results=None):
        output = {
            "source": "subfinder",
            "subdomains": [],
            "raw": "",
            "error": None,
        }

        if not self.available():
            output["error"] = "subfinder binary not found"
            return output

        try:
            host = target.replace("https://", "").replace("http://", "").split("/")[0]

            cmd = [
                self.binary,
                "-d",
                host,
                "-silent",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            raw = (proc.stdout or "").strip()
            output["raw"] = raw

            subs = []
            for line in raw.splitlines():
                line = line.strip()
                if line:
                    subs.append(line)

            output["subdomains"] = sorted(set(subs))

        except Exception as e:
            output["error"] = str(e)

        return output