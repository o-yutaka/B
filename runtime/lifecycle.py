"""Runtime lifecycle coordinator for Phase 3 adapters."""
from typing import Any, Iterable, Mapping
from events.event_types import EventType
from .dispatcher import Dispatcher, EventEnvelope

class RuntimeLifecycle:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher
        self._adapters: list[Any] = []

    def initialize(self, adapters: Iterable[Any], config: Mapping[str, Any] | None = None) -> None:
        self._adapters = list(adapters)
        for adapter in self._adapters:
            adapter.initialize(config or {})
            adapter.register(self, self._dispatcher)
            adapter.subscribe(self._dispatcher)
        self._dispatcher.publish(EventEnvelope(EventType.RUNTIME_INITIALIZED.value, metadata={"adapters": [a.name for a in self._adapters]}))

    def shutdown(self) -> None:
        for adapter in reversed(self._adapters):
            adapter.shutdown()
        self._dispatcher.publish(EventEnvelope(EventType.RUNTIME_SHUTDOWN.value))
