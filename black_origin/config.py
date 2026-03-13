from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "memory"
STATIC_DIR = BASE_DIR / "static"

MEMORY_FILES = {
    "planetary_index": DATA_DIR / "planetary_index.json",
    "knowledge_graph": DATA_DIR / "knowledge_graph.json",
    "causal_graph": DATA_DIR / "causal_graph.json",
    "world_model": DATA_DIR / "world_model.json",
    "event_stream": DATA_DIR / "event_stream.json",
    "sensor_data": DATA_DIR / "sensor_data.json",
    "research_memory": DATA_DIR / "research_memory.json",
}

HOST = "0.0.0.0"
PORT = 8000
LOOP_INTERVAL_SECONDS = 5
