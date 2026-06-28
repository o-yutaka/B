"""Adapter connecting IKernel to runtime events."""
from typing import Any
from events.event_types import EventType
from .base import RuntimeAdapter

class KernelAdapter(RuntimeAdapter):
    name = "adapter.kernel"
    input_event = EventType.DECISION_VALIDATED.value
    output_event = EventType.DECISION_ACCEPTED.value

    def handle(self, payload: Any) -> Any:
        return self.subsystem.decide(payload)
