"""Adapter connecting IExplorer to runtime events."""
from typing import Any
from events.event_types import EventType
from .base import RuntimeAdapter

class ExplorerAdapter(RuntimeAdapter):
    name = "adapter.explorer"
    input_event = EventType.DECISION_CREATED.value
    output_event = EventType.EVIDENCE_CREATED.value

    def handle(self, payload: Any) -> Any:
        return self.subsystem.search(payload.intent, payload.reality, payload.constraints)
