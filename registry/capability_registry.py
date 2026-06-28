"""Capability registry skeleton for BLACK module discovery."""
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class CapabilityDescriptor:
    name: str
    provider: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    event_namespace: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("capability name is required")
        if not self.provider:
            raise ValueError("capability provider is required")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

class CapabilityRegistry:
    """Registers and looks up capability metadata; it never executes capabilities."""
    def __init__(self) -> None:
        self._capabilities: dict[str, CapabilityDescriptor] = {}

    def register(self, capability: CapabilityDescriptor) -> None:
        if capability.name in self._capabilities:
            raise ValueError(f"capability already registered: {capability.name}")
        self._capabilities[capability.name] = capability

    def lookup(self, name: str) -> CapabilityDescriptor | None:
        return self._capabilities.get(name)

    def metadata(self, name: str) -> Mapping[str, Any]:
        capability = self._capabilities[name]
        return capability.metadata

    def all(self) -> Mapping[str, CapabilityDescriptor]:
        return MappingProxyType(dict(self._capabilities))
