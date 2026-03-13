import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from black_origin.config import MEMORY_FILES


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


DEFAULT_MEMORY = {
    "planetary_index": {
        "updated_at": "",
        "datasets": [],
        "apis": [],
        "entities": [],
        "topics": [],
    },
    "knowledge_graph": {
        "updated_at": "",
        "entities": [],
        "relationships": [],
    },
    "causal_graph": {
        "updated_at": "",
        "links": [],
        "evidence": [],
    },
    "world_model": {
        "updated_at": "",
        "domains": {
            "economy": {"signal": 0.0},
            "energy": {"signal": 0.0},
            "climate": {"signal": 0.0},
            "technology": {"signal": 0.0},
            "population": {"signal": 0.0},
            "geopolitics": {"signal": 0.0},
            "resources": {"signal": 0.0},
        },
        "scenarios": [],
        "predictions": [],
    },
    "event_stream": {"updated_at": "", "events": []},
    "sensor_data": {"updated_at": "", "sensors": []},
    "research_memory": {"updated_at": "", "insights": [], "improvements": []},
}


class MemoryStore:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._bootstrap()

    def _bootstrap(self) -> None:
        for key, path in MEMORY_FILES.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                self.write(key, DEFAULT_MEMORY[key])

    def read(self, name: str) -> Dict[str, Any]:
        path = MEMORY_FILES[name]
        with self._lock:
            with path.open("r", encoding="utf-8") as fh:
                return json.load(fh)

    def write(self, name: str, payload: Dict[str, Any]) -> None:
        path = MEMORY_FILES[name]
        with self._lock:
            with path.open("w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2, ensure_ascii=False)

    def update(self, name: str, updater) -> Dict[str, Any]:
        with self._lock:
            current = self.read(name)
            updated = updater(current)
            updated["updated_at"] = utc_now()
            self.write(name, updated)
            return updated

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {name: self.read(name) for name in MEMORY_FILES}
