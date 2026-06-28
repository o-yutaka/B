"""Explicit dependency registration container without global state."""
from types import MappingProxyType
from typing import Any, Mapping

class ServiceLocator:
    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        if not name:
            raise ValueError("service name is required")
        if name in self._services:
            raise ValueError(f"service already registered: {name}")
        self._services[name] = service

    def resolve(self, name: str) -> Any:
        return self._services[name]

    def has(self, name: str) -> bool:
        return name in self._services

    def services(self) -> Mapping[str, Any]:
        return MappingProxyType(dict(self._services))
