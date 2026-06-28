"""Immutable EvidencePacket data contract."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class EvidencePacket:
    source: str
    trust_score: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Any = None
    provenance: Mapping[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    validation_state: str = "unvalidated"

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError("source is required")
        for name, value in (("trust_score", self.trust_score), ("confidence", self.confidence)):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0.0 and 1.0")
        object.__setattr__(self, "provenance", MappingProxyType(dict(self.provenance)))
