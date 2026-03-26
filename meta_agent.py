import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class MetaTask:
    task: str
    source: str
    score: int


class GoalMemory:
    def __init__(self, path: str = "goals.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(json.dumps({"current": [], "completed": [], "failed": []}, ensure_ascii=False, indent=2), encoding="utf-8")

    def _read(self) -> Dict[str, List[str]]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {"current": [], "completed": [], "failed": []}

    def add_goal(self, goal: str) -> None:
        data = self._read()
        if goal not in data["current"] and goal not in data["completed"]:
            data["current"].append(goal)
            self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def mark_completed(self, goal: str) -> None:
        data = self._read()
        if goal in data["current"]:
            data["current"].remove(goal)
        if goal not in data["completed"]:
            data["completed"].append(goal)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def mark_failed(self, goal: str) -> None:
        data = self._read()
        if goal in data["current"]:
            data["current"].remove(goal)
        data["failed"].append(goal)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def current(self) -> List[str]:
        return self._read().get("current", [])


class MetaAgent:
    def __init__(self, top_n: int = 5) -> None:
        self.top_n = top_n
        self.goal_memory = GoalMemory()

    def is_valid_task(self, task: str, seen: set[str]) -> bool:
        text = task.strip()
        if len(text) < 10:
            return False
        if text in seen:
            return False
        keywords = ["build", "create", "fix", "generate", "optimize", "改善", "実装", "分析", "設計"]
        return any(k in text.lower() for k in keywords) or any(k in text for k in ["改善", "実装", "分析", "設計"])

    def score_task(self, task: str, source: str) -> int:
        s = 0
        low = task.lower()
        if "error" in low or "失敗" in low:
            s += 10
        if source == "user":
            s += 8
        if "optimiz" in low or "最適" in task:
            s += 5
        if len(task.strip()) < 20:
            s -= 5
        if task in self.goal_memory.current():
            s += 4
        return s

    def strategic_goals(self, external_signals: List[str]) -> List[str]:
        goals = []
        for signal in external_signals[:3]:
            goals.append(f"Create product idea and implementation plan for trend: {signal}")
        for g in goals:
            self.goal_memory.add_goal(g)
        return goals

    def filter_and_rank(self, tasks: List[Tuple[str, str]], seen: set[str]) -> List[MetaTask]:
        ranked: List[MetaTask] = []
        for task, source in tasks:
            if not self.is_valid_task(task, seen):
                continue
            ranked.append(MetaTask(task=task, source=source, score=self.score_task(task, source)))
        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked[: self.top_n]
