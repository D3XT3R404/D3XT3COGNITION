from dexter.core.context import ScanContext
from dexter.core.registry import EngineRegistry
from dexter.engines.technology_engine import TechnologyEngine
from dexter.engines.framework_engine import FrameworkEngine
from dexter.engines.version_engine import VersionEngine
from dexter.engines.header_engine import HeaderEngine
from dexter.engines.cookie_engine import CookieEngine
from dexter.engines.metadata_engine import MetadataEngine
from dexter.engines.fingerprint_engine import FingerprintEngine
from dexter.engines.knowledge_engine import KnowledgeEngine
from dexter.engines.security_headers_engine import SecurityHeadersEngine
from dexter.engines.comment_engine import CommentEngine
from dexter.engines.email_engine import EmailEngine
from dexter.engines.endpoint_engine import EndpointEngine
from dexter.engines.form_engine import FormEngine
from dexter.engines.evidence_engine import EvidenceEngine


class Scanner:

    def __init__(self):

        self.registry = EngineRegistry()

        self.registry.register(

            HeaderEngine()

        )

        self.registry.register(

            CookieEngine()

        )

        self.registry.register(

            MetadataEngine()

        )

        self.registry.register(

            SecurityHeadersEngine()

        )
        self.registry.register(
            TechnologyEngine()
            )
        
        self.registry.register(
            FrameworkEngine()
            )
        
        self.registry.register(
            VersionEngine()
            )
        
        self.registry.register(
            FingerprintEngine()
            )

        self.registry.register(
            KnowledgeEngine()
            )
        
        self.registry.register(
            EndpointEngine()
            )

        self.registry.register(
            FormEngine()
            )

        self.registry.register(
            CommentEngine()
            )

        self.registry.register(
            EmailEngine()
            )

        self.registry.register(
            EvidenceEngine()
            )

    def scan(self, target, deep=False):

        context = ScanContext(target)

        self.registry.run(context)

        return context.results