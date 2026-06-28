"""Reasoner lifecycle boundary for OpenMythos.

This module is part of the BLACK v1.0 architecture bootstrap.
It intentionally contains typed lifecycle placeholders only.
Future implementation must register through RuntimeEngine and communicate through EventBus events under `reasoner.openmythos`.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True)
class OpenMythosReasoner:
    """Public lifecycle interface for reasoner lifecycle boundary for openmythos.

    TODO: Inject RuntimeEngine and EventBus ports when implementation begins.
    TODO: Publish and subscribe only through namespaced events.
    """

    name: str = "reasoner.openmythos"

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
