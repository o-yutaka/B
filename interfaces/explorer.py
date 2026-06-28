from abc import abstractmethod
from typing import Any, Mapping, Sequence
from .base import RuntimeCompatibleInterface
class IExplorer(RuntimeCompatibleInterface):
    event_namespace = "explorer"
    @abstractmethod
    def search(self, intent: Any, reality: Any, constraints: Sequence[Any] = ()) -> Sequence[Any]: ...
