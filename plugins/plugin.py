"""Plugin interface for BLACK v1.0 capabilities.

Capabilities must be loadable through the runtime plugin manager and communicate through EventBus events.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True)
class Plugin:
    """Required plugin lifecycle interface.

    TODO: Implement concrete plugin behavior only after RuntimeEngine registration contracts are finalized.
    """

    name: str

    def initialize(self, config: Mapping[str, Any] | None = None) -> None:
        """Prepare plugin dependencies."""
        ...

    def register(self, runtime: Any, event_bus: Any) -> None:
        """Register plugin with RuntimeEngine and EventBus."""
        ...

    def execute(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        """Execute plugin capability after an EventBus request."""
        ...

    def shutdown(self) -> None:
        """Release plugin resources."""
        ...
