from abc import abstractmethod
from typing import Any
from .base import RuntimeCompatibleInterface
class IGovernance(RuntimeCompatibleInterface):
    event_namespace = "governance"
    @abstractmethod
    def evaluate(self, decision_packet: Any) -> Any: ...
