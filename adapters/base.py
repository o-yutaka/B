"""Runtime adapter base for subsystem interface objects."""
from typing import Any, Mapping
from events.publishers import EventPublisher
from runtime.dispatcher import Dispatcher, EventEnvelope

class RuntimeAdapter:
    name = "adapter.base"
    input_event: str | None = None
    output_event: str | None = None

    def __init__(self, subsystem: Any) -> None:
        self.subsystem = subsystem
        self.publisher: EventPublisher | None = None
        self.initialized = False
        self.registered = False

    def initialize(self, config: Mapping[str, Any] | None = None) -> None:
        self.subsystem.initialize(config or {})
        self.initialized = True

    def register(self, runtime: Any, event_bus: Dispatcher) -> None:
        self.subsystem.register(runtime, event_bus)
        self.publisher = EventPublisher(event_bus)
        self.registered = True

    def subscribe(self, dispatcher: Dispatcher) -> None:
        if self.input_event is not None:
            dispatcher.subscribe(self.input_event, self.receive)

    def receive(self, envelope: EventEnvelope) -> None:
        result = self.handle(envelope.payload)
        if self.output_event and self.publisher:
            self.publisher.publish(self.output_event, result, metadata={"adapter": self.name, "source_event": envelope.event_type})

    def handle(self, payload: Any) -> Any:
        return payload

    def health(self) -> Mapping[str, str]:
        return self.subsystem.health()

    def shutdown(self) -> None:
        self.subsystem.shutdown()
