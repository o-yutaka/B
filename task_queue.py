import heapq
import time
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass(order=True)
class QueueTask:
    priority_score: float
    created_at: float
    task: str = field(compare=False)
    source: str = field(compare=False, default="random")
    urgency: int = field(compare=False, default=1)
    complexity: int = field(compare=False, default=1)
    failures: int = field(compare=False, default=0)


class TaskPriorityQueue:
    def __init__(self, recent_limit: int = 80, max_size: int = 200) -> None:
        self._heap: List[QueueTask] = []
        self._recent: List[str] = []
        self._recent_set: Set[str] = set()
        self.recent_limit = recent_limit
        self.failure_history: Dict[str, int] = {}
        self.max_size = max_size

    def compute_metrics(self, task: str, source: str) -> tuple[int, int, int]:
        txt = task.lower()
        failures = self.failure_history.get(task, 0)
        urgency = 5 if ("error" in txt or "失敗" in txt or source == "error" or source == "user") else 2
        complexity = 4 if len(task) > 60 or any(x in txt for x in ["api", "service", "agent", "最適化", "optimize"]) else 2
        return urgency, complexity, failures

    def score(self, urgency: int, complexity: int, failures: int) -> float:
        return -(urgency * 2.0 + complexity * 1.0 + failures * 3.0)

    def push(self, task: str, source: str = "random") -> bool:
        key = task.strip()
        if not key or key in self._recent_set or len(self._heap) >= self.max_size:
            return False
        urgency, complexity, failures = self.compute_metrics(task, source)
        priority_score = self.score(urgency, complexity, failures)
        heapq.heappush(
            self._heap,
            QueueTask(
                priority_score=priority_score,
                created_at=time.time(),
                task=task,
                source=source,
                urgency=urgency,
                complexity=complexity,
                failures=failures,
            ),
        )
        self._remember(key)
        return True

    def pop(self) -> Tuple[str, str] | None:
        if not self._heap:
            return None
        q = heapq.heappop(self._heap)
        return q.task, q.source

    def mark_failure(self, task: str) -> None:
        self.failure_history[task] = self.failure_history.get(task, 0) + 1

    def _remember(self, task: str) -> None:
        self._recent.append(task)
        self._recent_set.add(task)
        if len(self._recent) > self.recent_limit:
            oldest = self._recent.pop(0)
            self._recent_set.discard(oldest)

    def size(self) -> int:
        return len(self._heap)
