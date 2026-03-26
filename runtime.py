import asyncio
import logging
import os
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from agents import CriticAgent, ExecutorAgent, OptimizerAgent, PlannerAgent, ProductGenerator, load_agent_models
from ai import run as ollama_run
from black_chimera_core import black_chimera_core
from evolution import SelfEvolutionEngine
from external import generate_external_tasks
from github_integration import GitHubAutomation
from memory import memory_store
from meta_agent import MetaAgent
from monitoring import SystemMonitor
from task_queue import TaskPriorityQueue

LOGGER = logging.getLogger("black_origin.runtime")
Subscriber = Callable[[Dict[str, Any]], Awaitable[None]]


def log_and_store(category: str, message: str, status: str = "info", extra: Dict[str, Any] | None = None) -> None:
    print(f"[{category}] {status}: {message}")
    memory_store.append(category, message, status, extra)


def notify(msg: str) -> None:
    import requests

    webhook = os.getenv("NOTIFY_WEBHOOK_URL", "").strip()
    line_token = os.getenv("LINE_NOTIFY_TOKEN", "").strip()
    if webhook:
        try:
            requests.post(webhook, json={"message": msg}, timeout=10)
        except Exception as exc:
            LOGGER.warning("Webhook通知失敗: %s", exc)
    if line_token:
        try:
            requests.post(
                "https://notify-api.line.me/api/notify",
                headers={"Authorization": f"Bearer {line_token}"},
                data={"message": msg},
                timeout=10,
            )
        except Exception as exc:
            LOGGER.warning("LINE通知失敗: %s", exc)


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Subscriber]] = {}

    def subscribe(self, event_name: str, callback: Subscriber) -> None:
        self._subscribers.setdefault(event_name, []).append(callback)

    async def publish(self, event_name: str, payload: Dict[str, Any]) -> None:
        log_and_store("event_bus", f"イベント発火: {event_name}", extra=payload)
        for callback in self._subscribers.get(event_name, []):
            await callback(payload)


class TaskIntelligenceEngine:
    def generate_task(self, context: str = "") -> str:
        return ollama_run(f"Generate next high-value coding task. Context: {context}", model=load_agent_models().get("planner", "phi3"))


class GoalGenerationEngine:
    def optimize_goal(self, context: str) -> str:
        prompt = f"次に改善すべきゴールを1つ提案してください。文脈: {context}"
        return ollama_run(prompt, model=load_agent_models().get("optimizer", "llama3"))


class AgentSystem:
    def __init__(self, event_bus: EventBus, task_queue: TaskPriorityQueue, mode: str = "NORMAL") -> None:
        self.event_bus = event_bus
        self.task_queue = task_queue
        self.agent_models = load_agent_models()
        self.mode = mode.upper()
        self.lightweight = os.getenv("LIGHTWEIGHT_MODE", "false").lower() == "true"
        if self.lightweight:
            self.agent_models = {k: "tinyllama" for k in self.agent_models.keys()}
        self.planner = PlannerAgent(self.agent_models.get("planner", "phi3"))
        self.executor = ExecutorAgent(self.agent_models.get("executor", "mistral"))
        self.critic = CriticAgent(self.agent_models.get("critic", "tinyllama"))
        self.optimizer = OptimizerAgent(self.agent_models.get("optimizer", "llama3"))
        self.max_retries = min(int(os.getenv("MAX_RETRIES", "2")), 3)
        self.agent_performance: Dict[str, Dict[str, float]] = {a: {"ok": 0, "fail": 0} for a in ["planner", "executor", "critic", "optimizer"]}

    def route_task(self, task: str) -> str:
        low = task.lower()
        if "error" in low or "失敗" in low:
            return "critic_first"
        if "optimize" in low or "最適" in low:
            return "optimizer_priority"
        return "planner_first"

    def choose_model_by_complexity(self, task: str) -> str:
        if len(task) < 40:
            return "tinyllama"
        if len(task) < 100:
            return "mistral"
        return "llama3"

    def adapt_models(self) -> None:
        ex = self.agent_performance["executor"]
        if ex["fail"] > ex["ok"] + 2:
            self.executor.model = "llama3"
        if ex["ok"] > ex["fail"] + 3:
            self.executor.model = "mistral"

    async def execute(self, task: str) -> Dict[str, Any]:
        log_and_store("task", "マルチエージェント実行開始", extra={"task": task})
        route = self.route_task(task)

        planner_msg: Dict[str, Any] = {"task": task, "status": "skipped", "result": "", "meta": {"agent": "planner"}}
        if route == "planner_first":
            planner_msg = (await asyncio.to_thread(self.planner.plan, task)).to_dict()
            await self.event_bus.publish("agent.planner.done", planner_msg)

        dynamic_model = self.choose_model_by_complexity(task)
        execution_result = ""
        success = False
        for attempt in range(1, self.max_retries + 2):
            execution_result = black_chimera_core.run(task, model=dynamic_model)
            if "エラー" not in execution_result and "error" not in execution_result.lower():
                success = True
                break
            self.task_queue.mark_failure(task)
            log_and_store("task", f"実行失敗リトライ: {attempt}", "error", {"task": task})

        executor_msg = (await asyncio.to_thread(self.executor.execute, task)).to_dict()
        executor_msg["result"] = execution_result
        await self.event_bus.publish("agent.executor.done", executor_msg)

        if route == "critic_first":
            critic_msg = (await asyncio.to_thread(self.critic.critique, task, executor_msg["result"])).to_dict()
            await self.event_bus.publish("agent.critic.done", critic_msg)
            if critic_msg["status"] == "needs_fix":
                self.task_queue.mark_failure(task)
        else:
            critic_future = asyncio.to_thread(self.critic.critique, task, executor_msg["result"])
            optimizer_future = asyncio.to_thread(self.optimizer.optimize, task, executor_msg["result"], "parallel optimization")
            critic_obj, optimizer_obj = await asyncio.gather(critic_future, optimizer_future)
            critic_msg = critic_obj.to_dict()
            optimizer_msg = optimizer_obj.to_dict()
            await self.event_bus.publish("agent.critic.done", critic_msg)
            await self.event_bus.publish("agent.optimizer.done", optimizer_msg)
            if route == "optimizer_priority" or critic_msg["status"] == "approved":
                execution_result = optimizer_msg["result"]

        critic_status = locals().get("critic_msg", {}).get("status", "needs_fix")
        final_status = "success" if success and (route == "optimizer_priority" or critic_status == "approved") else "needs_fix"
        self.agent_performance["executor"]["ok" if final_status == "success" else "fail"] += 1
        self.adapt_models()
        Path("generated.py").write_text(execution_result, encoding="utf-8")

        completed = {
            "task": task,
            "status": final_status,
            "result": execution_result,
            "planner": planner_msg,
            "route": route,
            "model": dynamic_model,
        }
        await self.event_bus.publish("task.completed", completed)
        return {"ok": True, **completed}


class RuntimeEngine:
    def __init__(self) -> None:
        self.mode = os.getenv("SYSTEM_MODE", "NORMAL").upper()
        self.event_bus = EventBus()
        self.task_engine = TaskIntelligenceEngine()
        self.goal_engine = GoalGenerationEngine()
        self.task_queue = TaskPriorityQueue(max_size=int(os.getenv("MAX_QUEUE_SIZE", "200")))
        self.agent_system = AgentSystem(self.event_bus, self.task_queue, mode=self.mode)
        self.product_generator = ProductGenerator()
        self.meta_agent = MetaAgent(top_n=int(os.getenv("META_TOP_N", "5")))
        self.evolution = SelfEvolutionEngine()
        self.monitor = SystemMonitor()
        self.github = GitHubAutomation()
        self.running = False
        self.loop_guard = 0
        self.prefetch_plan: Optional[asyncio.Task] = None
        self.seen_tasks: set[str] = set()
        self.new_tasks_per_cycle = int(os.getenv("MAX_NEW_TASKS_PER_CYCLE", "2"))
        self._setup_subscribers()

    def enqueue_task(self, task: str, source: str = "random") -> bool:
        ranked = self.meta_agent.filter_and_rank([(task, source)], self.seen_tasks)
        if not ranked:
            log_and_store("meta", "低価値/重複タスクを除外", "error", {"task": task, "source": source})
            return False
        best = ranked[0]
        added = self.task_queue.push(best.task, best.source)
        if added:
            self.seen_tasks.add(best.task)
            log_and_store("queue", "MetaAgent経由でタスク投入", extra={"task": best.task, "source": best.source, "score": best.score})
        return added

    def _black_loop(self, task: str) -> Dict[str, str]:
        analysis = ollama_run(f"ANALYSIS: Decompose task -> {task}")
        arena = ollama_run(f"ARENA: Generate 2 approaches for -> {task}")
        evolution = ollama_run(f"EVOLUTION: Pick best pattern from -> {arena}")
        design = ollama_run(f"DESIGN: Create execution plan for -> {task}")
        return {"analysis": analysis, "arena": arena, "evolution": evolution, "design": design}

    def generate_product(self, request_text: str) -> Dict[str, Any]:
        value_score = self.meta_agent.score_task(f"optimize build product {request_text}", "user")
        if value_score < 5:
            return {"error": "価値スコア不足のため生成をスキップ"}
        product = self.product_generator.generate(request_text, model=self.agent_system.executor.model)
        if "files" in product and "README.md" not in product["files"]:
            product["files"]["README.md"] = "# Generated Product\n\n## Setup\n1. install\n2. run"
            product.setdefault("run_steps", []).append("README.md の手順に従って起動")
        log_and_store("product", "プロダクト生成完了", "success", {"request": request_text, "file_tree": product.get("file_tree", [])})
        return product

    def trigger_auto_pr(self, title: str, body: str) -> Dict[str, str]:
        result = self.github.auto_pr(title=title, body=body, base=os.getenv("GITHUB_BASE", "main"))
        status = "success" if result.get("ok") == "true" else "error"
        log_and_store("github", "自動PR実行", status, result)
        return result

    def _setup_subscribers(self) -> None:
        async def on_completed(payload: Dict[str, Any]) -> None:
            success = payload.get("status") == "success"
            self.monitor.mark_result(success)
            if success:
                goal = self.goal_engine.optimize_goal(f"成功したタスク: {payload.get('task')}")
                self.meta_agent.goal_memory.mark_completed(payload.get("task", ""))
                log_and_store("runtime", "自己改善(成功経路)", "success", {"goal": goal})
                notify(f"BLACK ORIGIN: タスク成功 -> {payload.get('task')}")
                if self.mode != "SAFE":
                    self.enqueue_task(f"optimize {payload.get('task')}", "optimization")
            else:
                fix_task = f"error: {payload.get('task')} の失敗原因を修復"
                self.meta_agent.goal_memory.mark_failed(payload.get("task", ""))
                self.enqueue_task(fix_task, "error")
                self.task_queue.mark_failure(payload.get("task", ""))
                log_and_store("runtime", "自己修復タスク投入", "error", {"task": fix_task})
                notify(f"BLACK ORIGIN: タスク要修正 -> {payload.get('task')}")

        self.event_bus.subscribe("task.completed", on_completed)

    async def _prefetch_next_plan(self) -> None:
        auto_task = self.task_engine.generate_task(context="next-cycle")
        planned = await asyncio.to_thread(self.agent_system.planner.plan, auto_task)
        self.enqueue_task(planned.task, "random")
        log_and_store("planner", "先読み計画完了", extra=planned.to_dict())

    def _ingest_external_intelligence(self) -> None:
        external_tasks = generate_external_tasks()
        strategic_goals = self.meta_agent.strategic_goals(external_tasks)
        candidates = [(t, "external") for t in external_tasks + strategic_goals]
        ranked = self.meta_agent.filter_and_rank(candidates, self.seen_tasks)
        for item in ranked[: self.new_tasks_per_cycle]:
            self.enqueue_task(item.task, item.source)

    async def loop_once(self) -> Dict[str, Any]:
        if self.task_queue.size() == 0:
            self._ingest_external_intelligence()
            auto_task = self.task_engine.generate_task(context=str(memory_store.latest(5)))
            self.enqueue_task(auto_task, "random")

        next_task = self.task_queue.pop()
        if not next_task:
            return {"task": "", "result": {"ok": False, "status": "empty"}}

        task, source = next_task
        log_and_store("task", "優先キューからタスク取得", extra={"task": task, "source": source})
        black_stages = self._black_loop(task)
        memory_store.append("black_loop", "ANALYSIS→ARENA→EVOLUTION→DESIGN 完了", extra=black_stages)

        self.prefetch_plan = asyncio.create_task(self._prefetch_next_plan())
        result = await self.agent_system.execute(task)
        if self.prefetch_plan:
            await self.prefetch_plan

        learning = self.evolution.analyze(memory_store.latest(100))
        new_models = self.evolution.evolve(learning, self.agent_system.agent_models)
        self.agent_system.agent_models.update(new_models)
        metrics = self.monitor.metrics(self.task_queue.size())

        memory_store.append(
            "multi_agent",
            "Planner→Executor | Critic+Optimizer(並列) → Memory 完了",
            extra={"task": task, "status": result.get("status"), "monitor": metrics, "learning": learning},
        )
        return {"task": task, "source": source, "result": result, "metrics": metrics}

    async def start_loop(self) -> None:
        if self.running:
            return
        self.running = True
        self.loop_guard = 0
        log_and_store("runtime", f"インテリジェンスループ開始 mode={self.mode}")
        interval = int(os.getenv("LOOP_INTERVAL", "20"))
        if self.mode == "AGGRESSIVE":
            interval = max(5, interval // 2)
        if self.mode == "SAFE":
            interval = max(20, interval)
        while self.running:
            try:
                await self.loop_once()
                self.loop_guard += 1
                if self.loop_guard > int(os.getenv("MAX_LOOP_STEPS", "500")):
                    log_and_store("runtime", "ループ安全停止", "error", {"reason": "max loop steps"})
                    self.running = False
                    break
            except Exception as exc:
                LOGGER.exception("ループ例外: %s", exc)
                log_and_store("runtime", f"ループ例外: {exc}", "error", {"error": str(exc)})
            await asyncio.sleep(interval)

    def stop(self) -> None:
        self.running = False
        log_and_store("runtime", "インテリジェンスループ停止")


runtime_engine = RuntimeEngine()
