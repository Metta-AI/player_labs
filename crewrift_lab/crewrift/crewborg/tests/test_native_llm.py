import importlib.util
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from crewrift.crewborg.strategy.meeting.llm import build_meeting_llm_client_from_env


def test_native_meeting_clients_without_provider_keys(monkeypatch):
    calls = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            calls.append((self.path, self.headers.get("X-Coworld-Player-Slot"), body))
            text = json.dumps({"schema_version": 1, "action": "wait", "reason": "native", "confidence": 0.8})
            data = json.dumps({"id": "msg_native", "type": "message", "role": "assistant", "model": body["model"], "content": [{"type": "text", "text": text}], "stop_reason": "end_turn", "usage": {"input_tokens": 1, "output_tokens": 1}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *_):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        monkeypatch.setenv("COWORLD_LLM_ENDPOINT", f"http://127.0.0.1:{server.server_port}")
        monkeypatch.setenv("COWORLD_LLM_MODEL", "anthropic/claude-haiku-4.5")
        monkeypatch.setenv("CREWBORG_LLM_MODEL", "retired")
        monkeypatch.setenv("USE_BEDROCK", "1")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("CREWBORG_LLM_MEETINGS", raising=False)
        monkeypatch.delenv("SUSPECTRA_LLM_MEETINGS", raising=False)
        context = {"constraints": {"valid_vote_targets": ["skip"]}, "state": {"fallback_vote": "skip"}}
        try:
            result = build_meeting_llm_client_from_env().decide(context, trigger="meeting")
            assert result.decision.reason == "native"
            path = Path(__file__).resolve().parents[2] / "suspectra/llm_meeting.py"
            spec = importlib.util.spec_from_file_location("suspectra_native", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert module.decide(context)["reason"] == "native"
        finally:
            server.shutdown()
            thread.join()
    assert [(path, slot) for path, slot, _ in calls] == [("/v1/messages", None), ("/v1/messages", None)]
    assert all(body["model"] == "anthropic/claude-haiku-4.5" for _, _, body in calls)
