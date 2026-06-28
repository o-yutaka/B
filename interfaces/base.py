"""Shared abstract runtime-compatible interface primitives."""
from abc import ABC, abstractmethod
from typing import Any, Mapping

class RuntimeCompatibleInterface(ABC):
    """Lifecycle contract for modules registered by RuntimeEngine and wired through EventBus."""
    event_namespace: str

    @abstractmethod
    def initialize(self, config: Mapping[str, Any] | None = None) -> None: ...
    @abstractmethod
    def register(self, runtime: Any, event_bus: Any) -> None: ...
    @abstractmethod
    def health(self) -> Mapping[str, str]: ...
    @abstractmethod
    def shutdown(self) -> None: ...
