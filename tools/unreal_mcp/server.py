"""ONOKO_ARCANA Unreal MCP server.

Implements the small subset of MCP needed by Codex over stdio:
initialize, tools/list, tools/call, and ping.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable

import ue_remote


SERVER_NAME = "onoko-unreal-mcp"
SERVER_VERSION = "0.1.0"


def _json_text(value: Any) -> dict[str, str]:
    return {"type": "text", "text": json.dumps(value, ensure_ascii=False, indent=2)}


def _tool_result(value: Any, is_error: bool = False) -> dict[str, Any]:
    result = {"content": [_json_text(value)]}
    if is_error:
        result["isError"] = True
    return result


def _schema_number(default: float, description: str) -> dict[str, Any]:
    return {"type": "number", "default": default, "description": description, "minimum": 0.1, "maximum": 30}


TOOLS: list[dict[str, Any]] = [
    {
        "name": "ue_status",
        "description": "Discover a running Unreal Editor Python remote-execution node and report local ONOKO_ARCANA connection settings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wait_seconds": _schema_number(2.5, "How long to wait for Unreal Editor discovery responses."),
            },
        },
    },
    {
        "name": "ue_execute_python",
        "description": "Execute arbitrary Unreal Editor Python through the local Python Script Plugin remote-execution channel. Use only for deliberate Editor automation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code or expression to run inside the Unreal Editor Python environment."},
                "mode": {
                    "type": "string",
                    "enum": ["ExecuteFile", "ExecuteStatement", "EvaluateStatement", "file", "statement", "eval"],
                    "default": "ExecuteFile",
                },
                "wait_seconds": _schema_number(2.5, "How long to wait for a running Unreal Editor node."),
                "node_id": {"type": "string", "description": "Optional node_id from ue_status."},
                "unattended": {"type": "boolean", "default": True},
            },
            "required": ["code"],
        },
    },
    {
        "name": "ue_get_editor_snapshot",
        "description": "Capture a safe JSON summary of the open Unreal Editor world, selected actors, selected assets, and Phase 1 level availability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wait_seconds": _schema_number(2.5, "How long to wait for a running Unreal Editor node."),
            },
        },
    },
    {
        "name": "ue_run_phase1_smoke",
        "description": "Run an ONOKO_ARCANA Phase 1 Unreal Editor smoke probe for map availability and required C++ runtime classes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wait_seconds": _schema_number(2.5, "How long to wait for a running Unreal Editor node."),
            },
        },
    },
    {
        "name": "ue_launch_editor",
        "description": "Launch the ONOKO_ARCANA Unreal Editor project using the configured UE 5.7 editor executable.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "additional_args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional extra UnrealEditor.exe arguments.",
                },
            },
        },
    },
]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    wait_seconds = float(arguments.get("wait_seconds", 2.5))
    handlers: dict[str, Callable[[], Any]] = {
        "ue_status": lambda: ue_remote.discover(wait_seconds=wait_seconds),
        "ue_execute_python": lambda: ue_remote.execute_python(
            code=str(arguments["code"]),
            mode=str(arguments.get("mode", "ExecuteFile")),
            wait_seconds=wait_seconds,
            node_id=arguments.get("node_id"),
            unattended=bool(arguments.get("unattended", True)),
        ),
        "ue_get_editor_snapshot": lambda: ue_remote.get_editor_snapshot(wait_seconds=wait_seconds),
        "ue_run_phase1_smoke": lambda: ue_remote.run_phase1_smoke(wait_seconds=wait_seconds),
        "ue_launch_editor": lambda: ue_remote.launch_editor(arguments.get("additional_args") or []),
    }
    if name not in handlers:
        return _tool_result({"error": f"Unknown tool: {name}"}, is_error=True)
    try:
        value = handlers[name]()
        is_error = False
        if name != "ue_status" and isinstance(value, dict):
            is_error = not bool(value.get("ok", True))
        return _tool_result(value, is_error=is_error)
    except Exception as exc:  # pragma: no cover - returned over MCP
        return _tool_result({"error": f"{type(exc).__name__}: {exc}"}, is_error=True)


def read_message() -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if line == b"":
            return None
        line_text = line.decode("ascii", errors="replace").strip()
        if not line_text:
            break
        if ":" in line_text:
            key, value = line_text.split(":", 1)
            headers[key.lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def write_message(message: dict[str, Any]) -> None:
    body = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def response(request_id: Any, result: Any = None, error: Any = None) -> dict[str, Any]:
    payload = {"jsonrpc": "2.0", "id": request_id}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    return payload


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        protocol = params.get("protocolVersion", "2024-11-05")
        return response(
            request_id,
            {
                "protocolVersion": protocol,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return response(request_id, {})
    if method == "tools/list":
        return response(request_id, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        return response(request_id, call_tool(name, arguments))
    if request_id is None:
        return None
    return response(request_id, error={"code": -32601, "message": f"Method not found: {method}"})


def main() -> int:
    while True:
        message = read_message()
        if message is None:
            return 0
        reply = handle(message)
        if reply is not None:
            write_message(reply)


if __name__ == "__main__":
    raise SystemExit(main())
