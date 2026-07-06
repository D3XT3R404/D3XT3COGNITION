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

    def build_basic_registry(self):
        registry = EngineRegistry()
        registry.register(TechnologyEngine())
        registry.register(FrameworkEngine())
        registry.register(VersionEngine())
        registry.register(FingerprintEngine())
        registry.register(KnowledgeEngine())
        return registry

    def build_deep_registry(self):
        registry = EngineRegistry()
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

    def iter_scan(self, target, deep=False):
        context = ScanContext(target, deep)
        context.results["target"] = context.target
        context.results["host"] = context.hostname

        # capture dulu
        for engine in self.build_capture_registry().engines:
            name = engine.name
            try:
                data = engine.run(context)
                context.results[name] = data
            except Exception as e:
                data = {"error": str(e)}
                context.results[name] = data
            yield name, data

        # basic correlation
        for engine in self.build_basic_registry().engines:
            name = engine.name
            try:
                data = engine.run(context)
                context.results[name] = data
            except Exception as e:
                data = {"error": str(e)}
                context.results[name] = data
            yield name, data

        if deep:
            # adapter dulu
            adapters_result = self.adapter_manager.run(context.target, context.results)
            context.results.update(adapters_result)
            for adapter_name in adapters_result:
                yield adapter_name, adapters_result[adapter_name]

            # deep correlation setelah adapter
            for engine in self.build_deep_registry().engines:
                name = engine.name
                try:
                    data = engine.run(context)
                    context.results[name] = data
                except Exception as e:
                    data = {"error": str(e)}
                    context.results[name] = data
                yield name, data

        return context.results

    def scan(self, target, deep=False):
        final = None
        for name, data in self.iter_scan(target, deep=deep):
            final = (name, data)
        return final