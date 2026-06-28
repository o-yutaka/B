"""Canonical runtime event names for BLACK Phase 3."""
from enum import StrEnum

class EventType(StrEnum):
    RUNTIME_INITIALIZED = "runtime.initialized"
    RUNTIME_SHUTDOWN = "runtime.shutdown"
    DECISION_CREATED = "decision.created"
    DECISION_VALIDATED = "decision.validated"
    DECISION_ACCEPTED = "decision.accepted"
    DECISION_REJECTED = "decision.rejected"
    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    FEEDBACK_RECEIVED = "feedback.received"
    MEMORY_UPDATED = "memory.updated"
    COMPRESSION_COMPLETED = "compression.completed"
    EVIDENCE_CREATED = "evidence.created"
    PACKET_ROUTED = "packet.routed"

CANONICAL_EVENTS = tuple(event.value for event in EventType)
