"""Immutable ExecutionPacket data contract."""
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class ExecutionPacket:
    execution_id: str
    decision_id: str
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    priority: int = 0
    deadline: datetime | None = None
    status: str = "pending"

    def __post_init__(self) -> None:
        if not self.execution_id:
            raise ValueError("execution_id is required")
        if not self.decision_id:
            raise ValueError("decision_id is required")
        if not self.action:
            raise ValueError("action is required")
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))
