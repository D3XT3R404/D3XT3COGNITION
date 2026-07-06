import json
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class WPScanAdapter(BaseAdapter):
    binary = "wpscan"

    def execute(self, target, results=None):
        output = {
            "source": "wpscan",
            "wordpress": {
                "detected": False,
                "version": None,
                "plugins": [],
                "themes": [],
                "users": [],
                "interesting_findings": [],
            },
            "raw": "",
            "error": None,
        }

        if not self.available():
            output["error"] = "wpscan binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "--url", target,
                "--format", "json",
                "--no-banner",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )

            raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
            output["raw"] = raw.strip()

            data = None
            try:
                data = json.loads(proc.stdout)
            except Exception:
                data = None

            if not data:
                return output

            wp = output["wordpress"]
            wp["detected"] = True

            if isinstance(data, dict):
                wp["version"] = data.get("version") or data.get("wp_version")

                plugins = data.get("plugins", {})
                if isinstance(plugins, dict):
                    for plugin_name, plugin_data in plugins.items():
                        wp["plugins"].append({
                            "name": plugin_name,
                            "version": plugin_data.get("version"),
                            "vulnerabilities": plugin_data.get("vulnerabilities", []),
                        })

                themes = data.get("themes", {})
                if isinstance(themes, dict):
                    for theme_name, theme_data in themes.items():
                        wp["themes"].append({
                            "name": theme_name,
                            "version": theme_data.get("version"),
                            "vulnerabilities": theme_data.get("vulnerabilities", []),
                        })

                users = data.get("users", [])
                if isinstance(users, list):
                    wp["users"] = users

                findings = data.get("interesting_findings", [])
                if isinstance(findings, list):
                    wp["interesting_findings"] = findings

        except Exception as e:
            output["error"] = str(e)

        return output