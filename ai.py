import json
import logging
import os
import time
from threading import Lock
from typing import Optional

import requests

LOGGER = logging.getLogger("black_origin.ai")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")
MODEL = os.getenv("MODEL", "mistral")
TIMEOUT = 30


class OllamaClient:
    def __init__(self, model: Optional[str] = None, url: Optional[str] = None) -> None:
        self.model = model or os.getenv("MODEL", MODEL)
        self.url = url or os.getenv("OLLAMA_URL", OLLAMA_URL)
        self.base_url = os.getenv("OLLAMA_BASE", OLLAMA_BASE)
        self._known_models: set[str] = set()
        self._lock = Lock()

    def _tags(self) -> dict:
        response = requests.get(f"{self.base_url}/api/tags", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def wait_until_ready(self, retries: int = 10, interval: int = 1) -> tuple[bool, str]:
        for attempt in range(1, retries + 1):
            try:
                self._tags()
                return True, "Ollama準備完了"
            except Exception as exc:
                LOGGER.warning("Ollama接続待機中: 試行=%s エラー=%s", attempt, exc)
                time.sleep(interval)
        return False, "Ollama APIへ接続できません。Ollamaを起動してから再実行してください。"

    def ensure_model(self, model: Optional[str] = None) -> None:
        selected = (model or self.model).strip()
        with self._lock:
            if selected in self._known_models:
                return
            tags = self._tags()
            installed = {item.get("name", "") for item in tags.get("models", [])}
            model_found = any(name == selected or name.startswith(f"{selected}:") for name in installed)
            if model_found:
                LOGGER.info("Ollamaモデル確認済み: %s", selected)
                self._known_models.add(selected)
                return

            LOGGER.info("モデル未検出のため自動取得します: %s", selected)
            pull_payload = {"name": selected, "stream": False}
            pull_response = requests.post(f"{self.base_url}/api/pull", json=pull_payload, timeout=600)
            pull_response.raise_for_status()
            try:
                payload = pull_response.json()
                LOGGER.info("モデル取得結果: %s", json.dumps(payload, ensure_ascii=False)[:300])
            except Exception:
                LOGGER.info("モデル取得完了: %s", selected)
            self._known_models.add(selected)

    def ensure_ready(self) -> tuple[bool, str]:
        ready, message = self.wait_until_ready(retries=10, interval=1)
        if not ready:
            return False, message
        try:
            self.ensure_model(self.model)
            return True, "Ollama準備完了"
        except Exception as exc:
            LOGGER.error("モデル準備失敗: %s", exc)
            return False, "Ollamaモデルの準備に失敗しました。モデル設定を確認してください。"

    def generate(self, prompt: str, model: Optional[str] = None) -> str:
        ready, msg = self.wait_until_ready(retries=10, interval=1)
        if not ready:
            return msg

        selected_model = (model or self.model).strip()
        try:
            self.ensure_model(selected_model)
        except Exception as exc:
            LOGGER.exception("モデル準備失敗: %s", exc)
            return "AIモデル準備でエラーが発生しました。"

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            LOGGER.info("Ollamaへリクエスト送信: model=%s", selected_model)
            response = requests.post(self.url, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            text = data.get("response", "").strip()
            LOGGER.info("Ollama応答を受信: %s文字", len(text))
            return text or "応答が空です。"
        except Exception as exc:
            LOGGER.exception("Ollama呼び出し失敗: %s", exc)
            return "AI処理中にエラーが発生しました。しばらくして再試行してください。"


client = OllamaClient()


def ensure_ollama_ready() -> tuple[bool, str]:
    return client.ensure_ready()


def run(prompt: str, model: Optional[str] = None) -> str:
    return client.generate(prompt, model=model)
