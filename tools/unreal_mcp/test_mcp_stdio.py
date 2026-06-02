from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SERVER = Path(__file__).with_name("server.py")


def encode(message: dict) -> bytes:
    body = json.dumps(message, separators=(",", ":")).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def read_message(stream) -> dict:
    headers = {}
    while True:
        line = stream.readline()
        if line == b"":
            raise RuntimeError("server closed stdout")
        text = line.decode("ascii", errors="replace").strip()
        if not text:
            break
        if ":" in text:
            key, value = text.split(":", 1)
            headers[key.lower()] = value.strip()
    length = int(headers["content-length"])
    return json.loads(stream.read(length).decode("utf-8"))


def request(proc: subprocess.Popen, message: dict) -> dict:
    proc.stdin.write(encode(message))
    proc.stdin.flush()
    return read_message(proc.stdout)


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        print(json.dumps(request(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}}), ensure_ascii=False, indent=2))
        print(json.dumps(request(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}), ensure_ascii=False, indent=2))
        print(json.dumps(request(proc, {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ue_status", "arguments": {"wait_seconds": 1.0}}}), ensure_ascii=False, indent=2))
    finally:
        proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
