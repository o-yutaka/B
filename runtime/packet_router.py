"""Packet router that maps contract packets to canonical events."""
from typing import Any
from contracts import DecisionPacket, EvidencePacket, ExecutionPacket
from events.event_types import EventType
from .dispatcher import Dispatcher, EventEnvelope

class PacketRouter:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher
        self._routes: dict[type[Any], str] = {
            DecisionPacket: EventType.DECISION_CREATED.value,
            EvidencePacket: EventType.EVIDENCE_CREATED.value,
            ExecutionPacket: EventType.EXECUTION_STARTED.value,
        }

    def register_route(self, packet_type: type[Any], event_type: str) -> None:
        if not event_type:
            raise ValueError("event_type is required")
        self._routes[packet_type] = event_type

    def route(self, packet: Any) -> EventEnvelope:
        event_type = self._routes.get(type(packet))
        if event_type is None:
            raise ValueError(f"no route registered for packet type: {type(packet).__name__}")
        return self._dispatcher.publish(EventEnvelope(event_type=event_type, payload=packet, metadata={"router": "PacketRouter"}))
