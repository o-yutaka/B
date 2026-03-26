import json
import logging
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Deque, Dict, List

LOGGER = logging.getLogger("black_origin.memory")
MAX_MEMORY = 1000


class MemoryStore:
    def __init__(self, path: str = "memory.json", limit: int = MAX_MEMORY) -> None:
        self.path = Path(path)
        self.limit = min(limit, MAX_MEMORY)
        self._items: Deque[Dict[str, Any]] = deque(maxlen=self.limit)
        self._lock = Lock()
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                for item in raw[-self.limit :]:
                    self._items.append(item)
            LOGGER.info("メモリを読み込みました: %s件", len(self._items))
        except Exception as exc:
            LOGGER.exception("メモリ読込失敗: %s", exc)
            self.path.write_text("[]", encoding="utf-8")

    def append(self, category: str, message: str, status: str = "info", extra: Dict[str, Any] | None = None) -> None:
        record = {
            "time": datetime.now(timezone.utc).isoformat(),
            "category": category,
            "status": status,
            "message": message,
            "extra": extra or {},
        }
        with self._lock:
            self._items.append(record)
            safe_list = list(self._items)[-self.limit :]
            self.path.write_text(
                json.dumps(safe_list, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def latest(self, n: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._items)[-n:]

    def all(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._items)


memory_store = MemoryStore()
