import threading
import time
from typing import Any, Dict

from black_origin.agents.agent_system import AgentSystem
from black_origin.config import LOOP_INTERVAL_SECONDS
from black_origin.engines.causal_graph_engine import CausalGraphEngine
from black_origin.engines.data_engine import DataEngine
from black_origin.engines.event_engine import EventEngine
from black_origin.engines.kernel_engine import KernelEngine
from black_origin.engines.knowledge_graph_engine import KnowledgeGraphEngine
from black_origin.engines.planetary_data_discovery import PlanetaryDataDiscoveryEngine
from black_origin.engines.planetary_data_index import PlanetaryDataIndexEngine
from black_origin.engines.planetary_graph_engine import PlanetaryGraphEngine
from black_origin.engines.prediction_engine import PredictionEngine
from black_origin.engines.research_engine import ResearchEngine
from black_origin.engines.self_evolution_engine import SelfEvolutionEngine
from black_origin.engines.sensor_engine import SensorEngine
from black_origin.engines.simulation_engine import SimulationEngine
from black_origin.engines.world_model_engine import WorldModelEngine
from black_origin.storage.memory_store import MemoryStore


class BlackOriginRuntime:
    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.kernel = KernelEngine()
        self.discovery_engine = PlanetaryDataDiscoveryEngine()
        self.index_engine = PlanetaryDataIndexEngine()
        self.data_engine = DataEngine()
        self.event_engine = EventEngine()
        self.sensor_engine = SensorEngine()
        self.knowledge_engine = KnowledgeGraphEngine()
        self.causal_engine = CausalGraphEngine()
        self.world_model_engine = WorldModelEngine()
        self.simulation_engine = SimulationEngine()
        self.prediction_engine = PredictionEngine()
        self.agent_system = AgentSystem()
        self.research_engine = ResearchEngine()
        self.evolution_engine = SelfEvolutionEngine()
        self.planetary_graph_engine = PlanetaryGraphEngine()

        self._graph_state: Dict[str, Any] = {"nodes": [], "links": [], "causal_links": [], "hotspots": []}
        self._lock = threading.RLock()
        self._running = False

    def run_cycle(self) -> Dict[str, Any]:
        heartbeat = self.kernel.tick()
        discoveries = self.discovery_engine.discover(heartbeat.cycle)
        normalized = self.data_engine.normalize_entities(discoveries)
        events = self.event_engine.generate_events(normalized, heartbeat.cycle)

        index = self.memory.update("planetary_index", lambda state: self.index_engine.update_index(state, discoveries))
        event_stream = self.memory.update("event_stream", lambda state: {**state, "events": (state["events"] + events)[-200:]})
        sensors = self.sensor_engine.synthesize_sensors(event_stream["events"])
        sensor_state = self.memory.update("sensor_data", lambda state: {**state, "sensors": sensors})

        knowledge = self.memory.update("knowledge_graph", lambda state: self.knowledge_engine.update_graph(state, normalized))
        causal = self.memory.update("causal_graph", lambda state: self.causal_engine.infer(state, heartbeat.cycle))

        world_model = self.memory.update(
            "world_model",
            lambda state: self.world_model_engine.update(state, sensor_state["sensors"], causal["links"]),
        )
        simulation = self.simulation_engine.run(world_model, heartbeat.cycle)
        prediction = self.prediction_engine.generate(simulation, causal["links"])

        world_model = self.memory.update(
            "world_model",
            lambda state: {**state, "scenarios": (state["scenarios"] + [simulation])[-30:], "predictions": (state["predictions"] + [prediction])[-30:]},
        )

        agent_outputs = self.agent_system.run(prediction)
        research = self.memory.update("research_memory", lambda state: self.research_engine.run(state, world_model, prediction))
        research = self.memory.update(
            "research_memory",
            lambda state: self.evolution_engine.evolve(state, agent_outputs),
        )

        graph_state = self.planetary_graph_engine.render_state(knowledge, causal, event_stream["events"])
        with self._lock:
            self._graph_state = graph_state

        return {
            "heartbeat": heartbeat.__dict__,
            "discoveries": len(discoveries),
            "events": len(events),
            "index_topics": index["topics"],
            "prediction": prediction,
            "agents": agent_outputs,
            "research_updates": len(research["insights"]),
        }

    def start_background_loop(self, interval: int = LOOP_INTERVAL_SECONDS) -> None:
        if self._running:
            return
        self._running = True

        def _loop():
            while self._running and self.kernel.system_alive:
                self.run_cycle()
                time.sleep(interval)

        thread = threading.Thread(target=_loop, daemon=True, name="black-origin-loop")
        thread.start()

    def snapshot(self) -> Dict[str, Any]:
        state = self.memory.snapshot()
        with self._lock:
            graph = self._graph_state
        state["planetary_graph"] = graph
        state["kernel"] = {"cycle": self.kernel.cycle, "alive": self.kernel.system_alive}
        return state
