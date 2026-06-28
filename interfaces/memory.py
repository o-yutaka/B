from abc import abstractmethod
from typing import Any, Sequence
from .base import RuntimeCompatibleInterface
class IMemory(RuntimeCompatibleInterface):
    event_namespace = "memory"
    @abstractmethod
    def store(self, record: Any) -> str: ...
    @abstractmethod
    def recall(self, query: Any) -> Sequence[Any]: ...
