import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class SelfEvolutionEngine:
    def __init__(self, path: str = "evolution_state.json") -> None:
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text(json.dumps({"history": [], "model_preference": {}}, ensure_ascii=False, indent=2), encoding="utf-8")

    def analyze(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        failures = [x for x in logs if x.get("status") == "error"]
        successes = [x for x in logs if x.get("status") == "success"]
        failure_rate = len(failures) / max(1, len(logs))
        return {
            "failure_rate": failure_rate,
            "success_count": len(successes),
            "failure_patterns": [x.get("message", "") for x in failures[-5:]],
        }

    def evolve(self, metrics: Dict[str, Any], current_models: Dict[str, str]) -> Dict[str, str]:
        new_models = current_models.copy()
        if metrics.get("failure_rate", 0) > 0.4:
            new_models["executor"] = "llama3"
            new_models["critic"] = "llama3"
        elif metrics.get("failure_rate", 0) < 0.2:
            new_models["critic"] = "tinyllama"
        self._persist(metrics, new_models)
        return new_models

    def _persist(self, metrics: Dict[str, Any], models: Dict[str, str]) -> None:
        state = json.loads(self.path.read_text(encoding="utf-8"))
        entry = {
            "time": datetime.utcnow().isoformat(),
            "metrics": metrics,
            "models": models,
        }
        state["history"].append(entry)
        state["history"] = state["history"][-100:]
        state["model_preference"] = models
        self.path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def versioned_update(self, content: str, prefix: str = "self_update") -> str:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = Path(f"{prefix}_{ts}.txt")
        path.write_text(content, encoding="utf-8")
        return str(path)
