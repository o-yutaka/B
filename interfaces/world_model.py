from abc import abstractmethod
from typing import Any, Sequence
from .base import RuntimeCompatibleInterface
class IWorldModel(RuntimeCompatibleInterface):
    event_namespace = "world_model"
    @abstractmethod
    def observe(self, observation: Any) -> None: ...
    @abstractmethod
    def simulate(self, candidate_actions: Sequence[Any]) -> Any: ...
