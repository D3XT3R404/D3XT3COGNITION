from dexter.core.adapter_manager import AdapterManager
from dexter.core.context import ScanContext
from dexter.core.scanner import Scanner


class FakeResponse:
    url = "http://example.test"
    headers = {
        "Server": "Apache/2.4.63",
        "X-Powered-By": "PHP/8.3.29",
        "Content-Type": "text/html; charset=utf-8",
    }
    cookies = []
    text = """
    <html>
      <head>
        <meta name="generator" content="WordPress 6.5">
        <script src="/wp-includes/js/jquery/jquery.min.js"></script>
        <link rel="stylesheet" href="/wp-content/themes/astra/style.css">
      </head>
      <body>
        <!-- TODO internal api token check -->
        <a href="/wp-json/">REST</a>
        admin@example.test
      </body>
    </html>
    """


def test_basic_scan_reuses_capture_response_and_detects_common_tech(monkeypatch):
    def fake_fetch(self, timeout=15):
        self.response = FakeResponse()
        self.target = FakeResponse.url
        return self.response

    monkeypatch.setattr(ScanContext, "fetch", fake_fetch)

    scanner = Scanner()
    scanner.adapter_manager = AdapterManager()

    sections = list(scanner.iter_scan("example.test", deep=False))
    results = dict(sections)

    assert "Apache" in results["technology"]
    assert "PHP" in results["technology"]
    assert "WordPress" in results["technology"]
    assert "jQuery" in results["technology"]
    assert results["emails"] == ["admin@example.test"]
    assert any("/wp-json/" in endpoint for endpoint in results["endpoints"])

    final = scanner.scan("example.test", deep=False)
    assert "technology" in final
    assert "evidence" in final


def test_adapter_manager_returns_only_adapter_results():
    manager = AdapterManager()
    existing_results = {"header": {"Server": "Apache"}}

    adapter_results = manager.run("example.test", existing_results)

    assert "header" not in adapter_results
    assert existing_results["adapters"] == adapter_results
