import asyncio
import logging
import os

from fastapi import FastAPI

from ai import ensure_ollama_ready
from memory import memory_store
from routes import router
from runtime import runtime_engine


def configure_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


configure_logging()
app = FastAPI(title="BLACK ORIGIN", description="WhatsApp連携AIオペレーティングシステム", version="1.0.0")
app.include_router(router)


@app.on_event("startup")
async def startup_event() -> None:
    ready, _ = ensure_ollama_ready()
    if ready:
        print("Ollama準備完了")
        memory_store.append("system", "Ollama準備完了", "success")
    else:
        print("Ollama接続失敗")
        memory_store.append("system", "Ollama接続失敗", "error")

    if os.getenv("AUTO_LOOP", "true").lower() == "true":
        asyncio.create_task(runtime_engine.start_loop())


@app.on_event("shutdown")
async def shutdown_event() -> None:
    runtime_engine.stop()
