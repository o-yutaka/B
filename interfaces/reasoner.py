from abc import abstractmethod
from typing import Any, Mapping
from .base import RuntimeCompatibleInterface
class IReasoner(RuntimeCompatibleInterface):
    event_namespace = "reasoner"
    @abstractmethod
    def reason(self, decision_packet: Any) -> Any: ...
