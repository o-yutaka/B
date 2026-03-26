import json
import os
from pathlib import Path
from threading import Lock
from typing import Dict


class AgentStateTracker:
    def __init__(self) -> None:
        home = Path.home()
        self.path = home / ".openclaw" / "openclaw.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._states: Dict[str, Dict[str, str]] = {}

    def update(self, name: str, emoji: str, model: str, status: str) -> None:
        with self._lock:
            self._states[name] = {
                "name": name,
                "emoji": emoji,
                "model": model,
                "status": status,
            }
            payload = {
                "system": "BLACK ORIGIN",
                "agents": list(self._states.values()),
            }
            self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def snapshot(self) -> Dict[str, Dict[str, str]]:
        with self._lock:
            return dict(self._states)


state_tracker = AgentStateTracker()
