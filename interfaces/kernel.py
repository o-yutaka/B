from abc import abstractmethod
from typing import Any
from .base import RuntimeCompatibleInterface
class IKernel(RuntimeCompatibleInterface):
    event_namespace = "kernel"
    @abstractmethod
    def decide(self, decision_packet: Any) -> Any: ...
