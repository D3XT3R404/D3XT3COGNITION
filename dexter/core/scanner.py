from dexter.core.context import ScanContext
from dexter.core.registry import EngineRegistry
from dexter.core.adapter_manager import AdapterManager

from dexter.engines.header_engine import HeaderEngine
from dexter.engines.cookie_engine import CookieEngine
from dexter.engines.metadata_engine import MetadataEngine
from dexter.engines.security_headers_engine import SecurityHeadersEngine
from dexter.engines.technology_engine import TechnologyEngine
from dexter.engines.framework_engine import FrameworkEngine
from dexter.engines.version_engine import VersionEngine
from dexter.engines.fingerprint_engine import FingerprintEngine
from dexter.engines.knowledge_engine import KnowledgeEngine
from dexter.engines.endpoints_engine import EndpointEngine
from dexter.engines.form_engine import FormEngine
from dexter.engines.comment_engine import CommentEngine
from dexter.engines.email_engine import EmailEngine
from dexter.engines.evidence_engine import EvidenceEngine

from dexter.engines.dns_engine import DnsEngine
from dexter.engines.tls_engine import TlsEngine
from dexter.engines.robots_engine import RobotsEngine
from dexter.engines.sitemap_engine import SitemapEngine
from dexter.engines.js_engine import JsEngine
from dexter.engines.cms_engine import CmsEngine
from dexter.engines.wordpress_engine import WordpressEngine
from dexter.engines.waf_engine import WafEngine
from dexter.engines.confidence_engine import ConfidenceEngine

from dexter.adapters.httpx_adapter import HttpxAdapter
from dexter.adapters.whatweb_adapter import WhatWebAdapter
from dexter.adapters.wpscan_adapter import WPScanAdapter
from dexter.adapters.wafw00f_adapter import Wafw00fAdapter
from dexter.adapters.katana_adapter import KatanaAdapter
from dexter.adapters.subfinder_adapter import SubfinderAdapter


class Scanner:
    def __init__(self):
        self.adapter_manager = AdapterManager()
        self.adapter_manager.register(HttpxAdapter())
        self.adapter_manager.register(WhatWebAdapter())
        self.adapter_manager.register(Wafw00fAdapter())
        self.adapter_manager.register(KatanaAdapter())
        self.adapter_manager.register(SubfinderAdapter())
        self.adapter_manager.register(WPScanAdapter())

    def build_capture_registry(self):
        registry = EngineRegistry()

        registry.register(HeaderEngine())
        registry.register(CookieEngine())
        registry.register(MetadataEngine())
        registry.register(SecurityHeadersEngine())
        registry.register(EndpointEngine())
        registry.register(FormEngine())
        registry.register(CommentEngine())
        registry.register(EmailEngine())
        registry.register(EvidenceEngine())

        return registry

    def build_correlation_registry(self, deep=False):
        registry = EngineRegistry()

        registry.register(TechnologyEngine())
        registry.register(FrameworkEngine())
        registry.register(VersionEngine())
        registry.register(FingerprintEngine())
        registry.register(KnowledgeEngine())

        if deep:
            registry.register(DnsEngine())
            registry.register(TlsEngine())
            registry.register(RobotsEngine())
            registry.register(SitemapEngine())
            registry.register(JsEngine())
            registry.register(CmsEngine())
            registry.register(WordpressEngine())
            registry.register(WafEngine())
            registry.register(ConfidenceEngine())

        return registry

    def scan(self, target, deep=False):
        context = ScanContext(target, deep)
        context.results["target"] = context.target
        context.results["host"] = context.hostname

        self.build_capture_registry().run(context)
        self.build_correlation_registry(deep=False).run(context)

        if deep:
            self.adapter_manager.run(context.target, context.results)
            self.build_correlation_registry(deep=True).run(context)

        return context.results