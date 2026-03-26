import logging
from typing import Optional

from ai import run as ollama_run
from memory import memory_store

LOGGER = logging.getLogger("black_origin.black_chimera")


class BlackChimeraServiceCore:
    """BLACK CHIMERA SERVICE CORE."""

    def __init__(self) -> None:
        self.last_result: Optional[str] = None

    def run(self, instruction: str, model: Optional[str] = None) -> str:
        """ローカルOllama HTTPを利用して実行。"""
        LOGGER.info("BLACK CHIMERA実行: %s", instruction)
        memory_store.append("black_chimera", f"実行要求: {instruction}", extra={"model": model or "default"})
        result = ollama_run(instruction, model=model)
        self.last_result = result
        memory_store.append("black_chimera", "実行完了", status="success", extra={"result": result[:500], "model": model or "default"})
        return result


black_chimera_core = BlackChimeraServiceCore()
