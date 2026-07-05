from dexter.core.registry import EngineRegistry
from dexter.core.adapter_manager import AdapterManager
from dexter.engines.dns_engine import DNSEngine
from dexter.engines.header_engine import HeaderEngine
from dexter.engines.cookie_engine import CookieEngine
from dexter.engines.tls_engine import TLSEngine
from dexter.engines.cms_engine import CMSEngine
from dexter.engines.framework_engine import FrameworkEngine
from dexter.engines.waf_engine import WAFEngine
from dexter.engines.metadata_engine import MetadataEngine
from dexter.engines.robots_engine import RobotsEngine
from dexter.engines.sitemap_engine import SitemapEngine
from dexter.reports.reporter import Reporter
from dexter.engines.version_engine import VersionEngine
from dexter.engines.knowledge_engine import KnowledgeEngine

from dexter.engines.security_headers_engine import (

    SecurityHeadersEngine

)

from dexter.engines.js_engine import (

    JSEngine

)
from dexter.core.correlation_engine import (

    CorrelationEngine

)


class Scanner:

    def __init__(

            self

    ):

        self.normal = (
            EngineRegistry()
        )

        self.deep = (
            EngineRegistry()
        )

        self.adapters = (
            AdapterManager()
        )
        self.reporter = (
            Reporter()
        )
        self.correlation = (
            CorrelationEngine()
        )
        self.version_engine = (
            VersionEngine()
        )
        self.knowledge_engine = (
            KnowledgeEngine()
        )

        ################################

        self.normal.register(
            DNSEngine()
        )

        self.normal.register(
            HeaderEngine()
        )

        self.normal.register(
            CookieEngine()
        )

        self.normal.register(
            TLSEngine()
        )

        self.normal.register(
            CMSEngine()
        )

        self.normal.register(
            FrameworkEngine()
        )

        self.normal.register(
            MetadataEngine()
        )

        ################################

        self.deep.register(
            WAFEngine()
        )

        self.deep.register(
            RobotsEngine()
        )

        self.deep.register(
            SitemapEngine()
        )

        self.deep.register(
            SecurityHeadersEngine()
        )

        self.deep.register(JSEngine())

    def scan(
            self,
            target,
            deep=False
            ):

        results = {}

        results["target"] = target

        results["mode"] = (
            "deep"
            if deep
            else
            "normal"
            )

        ################################

        print("[*] Running Normal Engines")

        normal = (
            self.normal.run(target)
        )
        results.update(normal)
        ################################

        if deep:
            print()
            print("[*] Deep Mode")

            deep_results = (
                self.deep.run(target)
            )

            results["deep"] = deep_results

        results["adapters"] = (
            self.adapters.run(target)
            )

        ################################

        results[
            "technologies"
            ] = (

    self.correlation.analyze(
        results
        )
        )

        results["knowledge"] = self.knowledge_engine.run(results)

        results["versions"] = (
            self.version_engine.run(
                results
                )
                )
        
        self.reporter.save(
            target,
            results
        )
        return results