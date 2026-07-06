class AdapterManager:
    def __init__(self):
        self.adapters = []

    def register(self, adapter):
        self.adapters.append(adapter)

    def _should_run_wpscan(self, results):
        if not isinstance(results, dict):
            return False

        wordpress = results.get("wordpress", {})
        cms = results.get("cms")
        technologies = results.get("technology", [])
        fingerprints = results.get("fingerprints", [])

        if isinstance(wordpress, dict) and wordpress.get("detected"):
            return True
        if cms == "WordPress":
            return True
        if "WordPress" in technologies:
            return True
        if "WordPress" in fingerprints:
            return True

        httpx = results.get("httpx", {})
        if isinstance(httpx, dict):
            for item in httpx.get("items", []):
                tech = item.get("tech", [])
                if any("wordpress" in str(t).lower() for t in tech):
                    return True

        whatweb = results.get("whatweb", {})
        if isinstance(whatweb, dict):
            for item in whatweb.get("detected", []):
                if str(item.get("name", "")).lower() == "wordpress":
                    return True

        return False

    def run(self, target, results=None):
        if results is None:
            results = {}

        results.setdefault("adapters", {})

        for adapter in self.adapters:
            adapter_name = adapter.name

            if not adapter.available():
                data = {"error": f"{adapter.binary or adapter.name} not found"}
                results[adapter_name] = data
                results["adapters"][adapter_name] = data
                continue

            if adapter_name == "wpscan" and not self._should_run_wpscan(results):
                continue

            adapter_target = target
            if adapter_name == "subfinder":
                adapter_target = adapter.host_only(target)
            else:
                adapter_target = adapter.normalize_target(target)

            try:
                data = adapter.execute(adapter_target, results=results)
            except Exception as e:
                data = {"error": str(e)}

            results[adapter_name] = data
            results["adapters"][adapter_name] = data

        return results