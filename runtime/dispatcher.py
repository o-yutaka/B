"""Event dispatcher used by the RuntimeEngine integration layer."""
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Callable, DefaultDict, Mapping
from uuid import uuid4

Subscriber = Callable[["EventEnvelope"], None]

@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_type: str
    payload: Any = None
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.event_type:
            raise ValueError("event_type is required")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

class Dispatcher:
    """Synchronous in-process event dispatcher for runtime packet connectivity.

    It provides event-bus semantics without embedding business logic. Subscribers receive
    immutable envelopes and may publish follow-up events through injected adapters.
    """
    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, list[Subscriber]] = defaultdict(list)
        self._published: list[EventEnvelope] = []

    def subscribe(self, event_type: str, subscriber: Subscriber) -> None:
        if not event_type:
            raise ValueError("event_type is required")
        if subscriber in self._subscribers[event_type]:
            return
        self._subscribers[event_type].append(subscriber)

    def publish(self, envelope: EventEnvelope) -> EventEnvelope:
        self._published.append(envelope)
        for subscriber in tuple(self._subscribers.get(envelope.event_type, ())):
            subscriber(envelope)
        return envelope

    def published(self) -> tuple[EventEnvelope, ...]:
        return tuple(self._published)

    def subscribers(self, event_type: str) -> tuple[Subscriber, ...]:
        return tuple(self._subscribers.get(event_type, ()))
