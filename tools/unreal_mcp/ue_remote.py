"""Small Unreal Editor remote-execution helper for ONOKO_ARCANA.

This module wraps Epic's bundled remote_execution.py so the MCP server can
discover a running Unreal Editor and execute Editor Python through the local
Python Script Plugin remote-execution channel.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENGINE_ROOT = Path(os.environ.get("ONOKO_UNREAL_ENGINE", r"<UE_5.7>"))
DEFAULT_PROJECT_PATH = REPO_ROOT / "Unreal" / "ONOKO_ARCANA" / "ONOKO_ARCANA.uproject"
UNREAL_PROJECT = Path(os.environ.get("ONOKO_UNREAL_PROJECT", str(DEFAULT_PROJECT_PATH)))
REMOTE_EXECUTION_DIR = Path(
    os.environ.get(
        "UE_REMOTE_EXECUTION_DIR",
        str(DEFAULT_ENGINE_ROOT / "Engine" / "Plugins" / "Experimental" / "PythonScriptPlugin" / "Content" / "Python"),
    )
)
AUDIT_LOG = REPO_ROOT / "reports" / "unreal-mcp-audit.jsonl"
CAPTURE_DIR = UNREAL_PROJECT.parent / "Saved" / "CodexMCP"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_remote_execution_module():
    if not REMOTE_EXECUTION_DIR.exists():
        raise FileNotFoundError(f"remote_execution.py directory not found: {REMOTE_EXECUTION_DIR}")
    remote_execution_file = REMOTE_EXECUTION_DIR / "remote_execution.py"
    if not remote_execution_file.exists():
        raise FileNotFoundError(f"remote_execution.py not found: {remote_execution_file}")
    path = str(REMOTE_EXECUTION_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)
    import remote_execution  # type: ignore

    return remote_execution


def settings_hint() -> dict[str, Any]:
    return {
        "project_config_section": "/Script/PythonScriptPlugin.PythonScriptPluginSettings",
        "required_project_settings": {
            "bRemoteExecution": True,
            "RemoteExecutionMulticastGroupEndpoint": "239.0.0.1:6766",
            "RemoteExecutionMulticastBindAddress": "127.0.0.1",
            "RemoteExecutionMulticastTtl": 0,
        },
        "editor_restart_note": "If the Editor was already open when DefaultEngine.ini changed, restart it or toggle Project Settings > Plugins > Python > Enable Remote Execution.",
    }


def _base_status() -> dict[str, Any]:
    return {
        "timestamp_utc": _now_iso(),
        "engine_root": str(DEFAULT_ENGINE_ROOT),
        "project": str(UNREAL_PROJECT),
        "remote_execution_dir": str(REMOTE_EXECUTION_DIR),
        "remote_execution_py_exists": str(REMOTE_EXECUTION_DIR / "remote_execution.py"),
        "settings_hint": settings_hint(),
    }


def discover(wait_seconds: float = 2.5) -> dict[str, Any]:
    status = _base_status()
    status["ok"] = False
    remote = None
    try:
        re = _load_remote_execution_module()
        remote = re.RemoteExecution()
        remote.start()
        deadline = time.time() + max(0.1, wait_seconds)
        nodes: list[dict[str, Any]] = []
        while time.time() < deadline:
            nodes = list(remote.remote_nodes)
            if nodes:
                break
            time.sleep(0.1)
        status["nodes"] = nodes
        status["node_count"] = len(nodes)
        status["ok"] = bool(nodes)
        if not nodes:
            status["message"] = "No Unreal Editor remote-execution node was discovered on 127.0.0.1."
        return status
    except Exception as exc:  # pragma: no cover - returned to MCP caller
        status["error"] = f"{type(exc).__name__}: {exc}"
        return status
    finally:
        if remote is not None:
            try:
                remote.stop()
            except Exception:
                pass


def _audit(event: dict[str, Any]) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {"timestamp_utc": _now_iso(), **event}
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _normalize_mode(mode: str, re_module: Any) -> str:
    aliases = {
        "file": re_module.MODE_EXEC_FILE,
        "exec": re_module.MODE_EXEC_FILE,
        "execute_file": re_module.MODE_EXEC_FILE,
        "statement": re_module.MODE_EXEC_STATEMENT,
        "execute_statement": re_module.MODE_EXEC_STATEMENT,
        "eval": re_module.MODE_EVAL_STATEMENT,
        "evaluate_statement": re_module.MODE_EVAL_STATEMENT,
    }
    if mode in {re_module.MODE_EXEC_FILE, re_module.MODE_EXEC_STATEMENT, re_module.MODE_EVAL_STATEMENT}:
        return mode
    lowered = mode.strip().lower()
    if lowered in aliases:
        return aliases[lowered]
    raise ValueError(
        "mode must be one of ExecuteFile, ExecuteStatement, EvaluateStatement, file, statement, or eval"
    )


def execute_python(
    code: str,
    mode: str = "ExecuteFile",
    wait_seconds: float = 2.5,
    node_id: str | None = None,
    unattended: bool = True,
) -> dict[str, Any]:
    result: dict[str, Any] = _base_status()
    result["ok"] = False
    result["mode"] = mode
    result["node_id"] = node_id
    remote = None
    try:
        re = _load_remote_execution_module()
        exec_mode = _normalize_mode(mode, re)
        _audit(
            {
                "tool": "ue_execute_python",
                "mode": exec_mode,
                "node_id": node_id,
                "code_preview": code[:500],
            }
        )
        remote = re.RemoteExecution()
        remote.start()
        deadline = time.time() + max(0.1, wait_seconds)
        nodes: list[dict[str, Any]] = []
        while time.time() < deadline:
            nodes = list(remote.remote_nodes)
            if nodes:
                break
            time.sleep(0.1)
        result["nodes"] = nodes
        if not nodes:
            result["message"] = "No Unreal Editor remote-execution node was discovered."
            return result
        selected = None
        if node_id:
            selected = next((node for node in nodes if node.get("node_id") == node_id), None)
            if selected is None:
                result["message"] = f"Requested node_id was not found: {node_id}"
                return result
        else:
            selected = nodes[0]
        result["selected_node"] = selected
        remote.open_command_connection(selected["node_id"])
        command_result = remote.run_command(code, unattended=unattended, exec_mode=exec_mode)
        result["command_result"] = command_result
        result["ok"] = bool(command_result.get("success", False))
        return result
    except Exception as exc:  # pragma: no cover - returned to MCP caller
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
    finally:
        if remote is not None:
            try:
                remote.stop()
            except Exception:
                pass


def _capture_script(payload: str, label: str, wait_seconds: float = 2.5) -> dict[str, Any]:
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    capture_path = CAPTURE_DIR / f"{label}-{uuid.uuid4().hex}.json"
    script = payload.replace("__CODEX_MCP_CAPTURE_PATH__", str(capture_path).replace("\\", "\\\\"))
    remote_result = execute_python(script, mode="ExecuteFile", wait_seconds=wait_seconds)
    combined = {"remote": remote_result, "capture_path": str(capture_path), "ok": False}
    if capture_path.exists():
        try:
            combined["data"] = json.loads(capture_path.read_text(encoding="utf-8"))
            combined["ok"] = bool(remote_result.get("ok"))
        except Exception as exc:
            combined["capture_error"] = f"{type(exc).__name__}: {exc}"
    return combined


SNAPSHOT_SCRIPT = r'''
import json
import os
import traceback

out_path = r"__CODEX_MCP_CAPTURE_PATH__"
data = {"ok": True, "errors": []}
try:
    import unreal

    data["engine_version"] = str(unreal.SystemLibrary.get_engine_version())
    data["project_dir"] = str(unreal.Paths.project_dir())
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world() if editor_subsystem else None
    data["world_name"] = world.get_name() if world else None
    data["world_path"] = world.get_path_name() if world else None

    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = list(actor_subsystem.get_all_level_actors()) if actor_subsystem else []
    selected_actors = list(actor_subsystem.get_selected_level_actors()) if actor_subsystem else []
    data["actor_count"] = len(actors)
    data["selected_actors"] = [actor.get_name() for actor in selected_actors]
    data["sample_actors"] = [actor.get_name() for actor in actors[:40]]

    try:
        selected_assets = list(unreal.EditorUtilityLibrary.get_selected_assets())
    except Exception as exc:
        selected_assets = []
        data["errors"].append("selected_assets: " + str(exc))
    data["selected_assets"] = [asset.get_path_name() for asset in selected_assets]

    try:
        data["phase1_level_exists"] = bool(
            unreal.EditorAssetLibrary.does_asset_exist("/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table")
        )
    except Exception as exc:
        data["errors"].append("phase1_level_exists: " + str(exc))
except Exception:
    data["ok"] = False
    data["traceback"] = traceback.format_exc()

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, ensure_ascii=False, indent=2)
'''


PHASE1_SMOKE_SCRIPT = r'''
import json
import os
import traceback

out_path = r"__CODEX_MCP_CAPTURE_PATH__"
data = {"ok": True, "checks": {}, "errors": []}

def check(name, value, detail=None):
    data["checks"][name] = {"ok": bool(value), "detail": detail}
    if not value:
        data["ok"] = False

try:
    import unreal

    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world() if editor_subsystem else None
    world_path = world.get_path_name() if world else ""
    data["engine_version"] = str(unreal.SystemLibrary.get_engine_version())
    data["world_path"] = world_path
    check("phase1_map_loaded_or_available", "/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table" in world_path or bool(unreal.EditorAssetLibrary.does_asset_exist("/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table")), world_path)

    for class_name in [
        "OnokoArcanaGameMode",
        "OnokoArcanaPlayerController",
        "OnokoArcanaTableController",
        "OnokoArcanaCardActor",
        "OnokoArcanaTableHudWidget",
    ]:
        cls = unreal.load_class(None, "/Script/ONOKO_ARCANA." + class_name)
        check("class_" + class_name, cls is not None, str(cls))

    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = list(actor_subsystem.get_all_level_actors()) if actor_subsystem else []
    data["actor_count"] = len(actors)
    data["actor_name_sample"] = [actor.get_name() for actor in actors[:50]]
except Exception:
    data["ok"] = False
    data["traceback"] = traceback.format_exc()

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as handle:
    json.dump(data, handle, ensure_ascii=False, indent=2)
'''


def get_editor_snapshot(wait_seconds: float = 2.5) -> dict[str, Any]:
    return _capture_script(SNAPSHOT_SCRIPT, "editor-snapshot", wait_seconds=wait_seconds)


def run_phase1_smoke(wait_seconds: float = 2.5) -> dict[str, Any]:
    return _capture_script(PHASE1_SMOKE_SCRIPT, "phase1-smoke", wait_seconds=wait_seconds)


def launch_editor(additional_args: list[str] | None = None) -> dict[str, Any]:
    editor_exe = DEFAULT_ENGINE_ROOT / "Engine" / "Binaries" / "Win64" / "UnrealEditor.exe"
    status = _base_status()
    status["ok"] = False
    status["editor_exe"] = str(editor_exe)
    if not editor_exe.exists():
        status["error"] = f"UnrealEditor.exe not found: {editor_exe}"
        return status
    if not UNREAL_PROJECT.exists():
        status["error"] = f"Project file not found: {UNREAL_PROJECT}"
        return status
    args = [str(editor_exe), str(UNREAL_PROJECT)]
    if additional_args:
        args.extend(additional_args)
    _audit({"tool": "ue_launch_editor", "args": args})
    proc = subprocess.Popen(args, cwd=str(UNREAL_PROJECT.parent), close_fds=True)
    status["ok"] = True
    status["pid"] = proc.pid
    status["args"] = args
    return status


if __name__ == "__main__":
    print(json.dumps(discover(), ensure_ascii=False, indent=2))
