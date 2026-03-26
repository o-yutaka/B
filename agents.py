import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict

from agent_state import state_tracker
from ai import run as ollama_run

LOGGER = logging.getLogger("black_origin.agents")

DEFAULT_AGENT_MODELS = {
    "planner": "phi3",
    "executor": "mistral",
    "critic": "tinyllama",
    "optimizer": "llama3",
}


def load_agent_models() -> Dict[str, str]:
    raw = os.getenv("AGENT_MODELS", "").strip()
    if not raw:
        return DEFAULT_AGENT_MODELS.copy()
    try:
        parsed = json.loads(raw)
        merged = DEFAULT_AGENT_MODELS.copy()
        for k, v in parsed.items():
            merged[k.lower()] = str(v)
        return merged
    except Exception:
        return DEFAULT_AGENT_MODELS.copy()


@dataclass
class AgentMessage:
    task: str
    status: str
    result: str
    meta: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "status": self.status,
            "result": self.result,
            "meta": self.meta,
        }


class BaseAgent:
    def __init__(self, name: str, emoji: str, model: str, personality: str, style: str, role: str, active_state: str) -> None:
        self.name = name
        self.emoji = emoji
        self.model = model
        self.personality = personality
        self.style = style
        self.role = role
        self.active_state = active_state
        self.set_state("idle")

    def set_state(self, status: str) -> None:
        state_tracker.update(self.name, self.emoji, self.model, status)

    def inject_personality(self, content: str) -> str:
        return (
            f"You are {self.personality}. "
            f"Style: {self.style}. "
            f"Role: {self.role}.\n"
            f"{content}"
        )


class PlannerAgent(BaseAgent):
    def __init__(self, model: str) -> None:
        super().__init__(
            name="PlannerAgent",
            emoji="🧠",
            model=model,
            personality="a strategic, abstract thinker",
            style="structured bullet points",
            role="break down tasks into steps",
            active_state="thinking",
        )

    def plan(self, goal: str) -> AgentMessage:
        self.set_state("thinking")
        prompt = self.inject_personality(
            "以下のゴールを実行可能な3つ以内のサブタスクへ分解してください。JSON配列で返してください。\n"
            f"ゴール: {goal}"
        )
        response = ollama_run(prompt, model=self.model)
        self.set_state("idle")
        return AgentMessage(task=goal, status="planned", result=response, meta={"agent": "planner", "model": self.model})


class ExecutorAgent(BaseAgent):
    def __init__(self, model: str) -> None:
        super().__init__(
            name="ExecutorAgent",
            emoji="🛠️",
            model=model,
            personality="a practical builder",
            style="direct and code-focused",
            role="generate and execute code",
            active_state="working",
        )

    def execute(self, task: str) -> AgentMessage:
        self.set_state("working")
        prompt = self.inject_personality(f"次のタスクを実行し、実装コードまたは実行手順を出力してください: {task}")
        response = ollama_run(prompt, model=self.model)
        self.set_state("idle")
        return AgentMessage(task=task, status="executed", result=response, meta={"agent": "executor", "model": self.model})


class CriticAgent(BaseAgent):
    def __init__(self, model: str) -> None:
        super().__init__(
            name="CriticAgent",
            emoji="🔍",
            model=model,
            personality="a strict analytical code reviewer",
            style="critical and concise",
            role="find bugs and inefficiencies",
            active_state="analyzing",
        )

    def critique(self, task: str, execution_result: str) -> AgentMessage:
        self.set_state("analyzing")
        prompt = self.inject_personality(
            "次の実行結果を評価し、バグと非効率を短く厳密に列挙してください。\n"
            f"タスク: {task}\n結果:\n{execution_result}"
        )
        response = ollama_run(prompt, model=self.model)
        lowered = response.lower()
        status = "needs_fix" if any(k in lowered for k in ["error", "bug", "失敗", "問題"]) else "approved"
        self.set_state("idle")
        return AgentMessage(task=task, status=status, result=response, meta={"agent": "critic", "model": self.model})


class OptimizerAgent(BaseAgent):
    def __init__(self, model: str) -> None:
        super().__init__(
            name="OptimizerAgent",
            emoji="✨",
            model=model,
            personality="a creative improver",
            style="enhancement-oriented",
            role="improve successful outputs",
            active_state="improving",
        )

    def optimize(self, task: str, execution_result: str, critique: str) -> AgentMessage:
        self.set_state("improving")
        prompt = self.inject_personality(
            "次の成果物を改善し、最適化版を返してください。\n"
            f"タスク: {task}\n成果物:\n{execution_result}\nレビュー:\n{critique}"
        )
        response = ollama_run(prompt, model=self.model)
        self.set_state("idle")
        return AgentMessage(task=task, status="optimized", result=response, meta={"agent": "optimizer", "model": self.model})


class ProductGenerator:
    def generate(self, request_text: str, model: str = "mistral") -> Dict[str, Any]:
        prompt = (
            "以下の要件からミニプロダクトを生成してください。"
            "必ずJSONで返し、keysは file_tree(list), files(dict), run_steps(list) とする。\n"
            f"要件: {request_text}\n"
            "対象タイプ: APIサービス / 小規模Webアプリ / 自動化スクリプト"
        )
        response = ollama_run(prompt, model=model)
        try:
            return json.loads(response)
        except Exception:
            return {
                "file_tree": ["generated_product/"],
                "files": {"generated_product/README.txt": response},
                "run_steps": ["生成結果を確認してください"],
            }
