"""Publication helpers for canonical runtime events."""
from typing import Any, Mapping
from runtime.dispatcher import Dispatcher, EventEnvelope

class EventPublisher:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher

    def publish(self, event_type: str, payload: Any = None, metadata: Mapping[str, Any] | None = None) -> EventEnvelope:
        return self._dispatcher.publish(EventEnvelope(event_type=event_type, payload=payload, metadata=metadata or {}))
