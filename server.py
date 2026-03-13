import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from black_origin.config import HOST, PORT, STATIC_DIR
from black_origin.runtime import BlackOriginRuntime

RUNTIME = BlackOriginRuntime()
RUNTIME.start_background_loop()


class BlackOriginHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/state":
            self._json(RUNTIME.snapshot())
            return
        if parsed.path == "/api/cycle":
            self._json(RUNTIME.run_cycle())
            return
        if parsed.path == "/api/chat":
            query = parse_qs(parsed.query)
            message = query.get("q", [""])[0].strip().lower()
            state = RUNTIME.snapshot()
            reply = self._chat_reply(message, state)
            self._json({"message": message, "reply": reply})
            return
        if parsed.path in {"/", "/index.html"}:
            self.path = "/index.html"
        return super().do_GET()

    @staticmethod
    def _chat_reply(message, state):
        if "prediction" in message:
            preds = state["world_model"]["predictions"]
            return preds[-1] if preds else {"info": "No predictions yet"}
        if "causal" in message:
            return state["causal_graph"]["links"][-5:]
        if "agent" in message:
            return {
                "agents": [
                    "collector_agent",
                    "analysis_agent",
                    "simulation_agent",
                    "strategy_agent",
                    "research_agent",
                ],
                "cycle": state["kernel"]["cycle"],
            }
        return {
            "status": "BLACK ORIGIN operational",
            "cycle": state["kernel"]["cycle"],
            "topics": state["planetary_index"]["topics"],
        }


def main():
    Path(STATIC_DIR).mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), BlackOriginHandler)
    print(f"BLACK ORIGIN serving on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
