"""Adapter connecting IMemory to runtime feedback and memory update events."""
from typing import Any
from events.event_types import EventType
from .base import RuntimeAdapter

class MemoryAdapter(RuntimeAdapter):
    name = "adapter.memory"
    input_event = EventType.FEEDBACK_RECEIVED.value
    output_event = EventType.MEMORY_UPDATED.value

    def handle(self, payload: Any) -> Any:
        return self.subsystem.store(payload)
