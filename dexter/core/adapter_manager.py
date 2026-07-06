class AdapterManager:
    def __init__(self):
        self.adapters = []

    def register(self, adapter):
        self.adapters.append(adapter)

    def run_all(self, target, results=None):
        collected = []

        for adapter in self.adapters:
            if not adapter.available():
                continue

            if adapter.name == "wpscan":
                wp_detected = False

                if isinstance(results, dict):
                    wordpress = results.get("wordpress", {})
                    cms = results.get("cms")
                    technologies = results.get("technology", [])

                    if isinstance(wordpress, dict) and wordpress.get("detected"):
                        wp_detected = True
                    elif cms == "WordPress":
                        wp_detected = True
                    elif "WordPress" in technologies:
                        wp_detected = True

                if not wp_detected:
                    continue

            try:
                data = adapter.execute(target, results=results)
                collected.append({
                    "adapter": adapter.name,
                    "data": data,
                })
            except Exception as e:
                collected.append({
                    "adapter": adapter.name,
                    "data": {
                        "error": str(e)
                    }
                })

        return collected