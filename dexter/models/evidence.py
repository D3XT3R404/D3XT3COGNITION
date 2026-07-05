from dataclasses import dataclass, field


@dataclass
class Evidence:

    engine: str

    type: str

    value: str

    confidence: int = 0

    source: str = ""

    extra: dict = field(default_factory=dict)