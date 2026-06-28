"""Adapter connecting IReasoner to runtime events."""
from typing import Any
from events.event_types import EventType
from .base import RuntimeAdapter

class ReasonerAdapter(RuntimeAdapter):
    name = "adapter.reasoner"
    input_event = EventType.EVIDENCE_CREATED.value
    output_event = EventType.DECISION_VALIDATED.value

    def handle(self, payload: Any) -> Any:
        return self.subsystem.reason(payload)
