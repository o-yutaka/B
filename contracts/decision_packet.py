"""Immutable DecisionPacket data contract."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping, Sequence

@dataclass(frozen=True, slots=True)
class DecisionPacket:
    decision_id: str
    intent: Any
    reality: Any
    evidence: Sequence[Any] = field(default_factory=tuple)
    constraints: Sequence[Any] = field(default_factory=tuple)
    candidate_actions: Sequence[Any] = field(default_factory=tuple)
    simulation: Any = None
    confidence: float = 0.0
    risk: float = 0.0
    verdict: str = "pending"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError("decision_id is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not 0.0 <= self.risk <= 1.0:
            raise ValueError("risk must be between 0.0 and 1.0")
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(self, "constraints", tuple(self.constraints))
        object.__setattr__(self, "candidate_actions", tuple(self.candidate_actions))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
