import json
import os
import subprocess

from dexter.adapters.base_adapter import BaseAdapter


class WPScanAdapter(BaseAdapter):
    binary = "wpscan"

    def execute(self, target, results=None):
        url = self.normalize_target(target)

        output = {
            "source": "wpscan",
            "wordpress": {
                "detected": False,
                "version": None,
                "theme": None,
                "plugins": [],
                "themes": [],
                "users": [],
                "interesting_findings": [],
                "plugin_details": {},
                "theme_details": {},
                "api_token_used": False,
            },
            "error": None,
        }

        if not self.available():
            output["error"] = "wpscan binary not found"
            return output

        try:
            cmd = [
                self.binary,
                "--url",
                url,
                "--format",
                "json",
                "--no-banner",
            ]

            token = None
            if isinstance(results, dict):
                token = results.get("wpscan_api_token")

            if not token:
                token = os.getenv("WPSCAN_API_TOKEN")

            if token:
                cmd.extend(["--api-token", token])
                output["wordpress"]["api_token_used"] = True

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
            )

            stdout = (proc.stdout or "").strip()
            stderr = (proc.stderr or "").strip()

            if proc.returncode != 0 and not stdout:
                output["error"] = stderr or f"wpscan exited with code {proc.returncode}"
                return output

            try:
                data = json.loads(stdout)
            except Exception:
                data = None

            if not isinstance(data, dict):
                if stdout:
                    output["error"] = stderr or "wpscan returned non-JSON output"
                return output

            if data.get("scan_aborted"):
                output["error"] = data.get("scan_aborted")
                return output

            wp = output["wordpress"]

            wp["version"] = data.get("version") or data.get("wp_version")
            wp["theme"] = data.get("theme") or data.get("active_theme")

            plugins = data.get("plugins", {})
            if isinstance(plugins, dict):
                for plugin_name, plugin_data in plugins.items():
                    wp["plugins"].append(plugin_name)
                    if isinstance(plugin_data, dict):
                        wp["plugin_details"][plugin_name] = {
                            "version": plugin_data.get("version"),
                            "vulnerabilities": plugin_data.get("vulnerabilities", []),
                        }

            themes = data.get("themes", {})
            if isinstance(themes, dict):
                for theme_name, theme_data in themes.items():
                    wp["themes"].append(theme_name)
                    if isinstance(theme_data, dict):
                        wp["theme_details"][theme_name] = {
                            "version": theme_data.get("version"),
                            "vulnerabilities": theme_data.get("vulnerabilities", []),
                        }

            users = data.get("users", [])
            if isinstance(users, list):
                wp["users"] = users

            findings = data.get("interesting_findings", [])
            if isinstance(findings, list):
                wp["interesting_findings"] = findings

            wp["detected"] = bool(
                wp["version"]
                or wp["plugins"]
                or wp["themes"]
                or wp["users"]
                or wp["interesting_findings"]
            )

            wp["plugins"] = sorted(set(wp["plugins"]))
            wp["themes"] = sorted(set(wp["themes"]))

        except Exception as e:
            output["error"] = str(e)

        return output
