"""Event bus interface boundary for BLACK v1.0 modules.

This module is part of the BLACK v1.0 architecture bootstrap.
It intentionally contains typed lifecycle placeholders only.
Future implementation must register through RuntimeEngine and communicate through EventBus events under `runtime.event_bus`.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True)
class EventBusPort:
    """Public lifecycle interface for event bus interface boundary for black v1.0 modules.

    TODO: Inject RuntimeEngine and EventBus ports when implementation begins.
    TODO: Publish and subscribe only through namespaced events.
    """

    name: str = "runtime.event_bus"

    def initialize(self, config: Mapping[str, Any] | None = None) -> None:
        """Prepare runtime-owned dependencies before registration."""
        ...

    def register(self, runtime: Any, event_bus: Any) -> None:
        """Register this module through RuntimeEngine and EventBus."""
        ...

    def health(self) -> Mapping[str, str]:
        """Return health metadata for runtime supervision."""
        ...

    def version(self) -> str:
        """Return the module contract version."""
        ...

    def shutdown(self) -> None:
        """Release runtime-owned resources during shutdown."""
        ...
