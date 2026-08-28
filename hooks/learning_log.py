#!/usr/bin/env python3
"""Append opt-in Codex hook events to the active Markdown learning note."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(os.environ.get("PLUGIN_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from learning_session import append_markdown, load_state, save_state, state_path  # noqa: E402


def callout(kind: str, title: str, text: str) -> str:
    lines = [f"> [!{kind}] {title}", ">"]
    lines.extend(">" if not line else f"> {line}" for line in text.strip().splitlines())
    return "\n".join(lines)


def hook_response() -> None:
    print(json.dumps({"continue": True, "suppressOutput": True}))


def handle(event: dict[str, Any]) -> None:
    cwd_raw = event.get("cwd")
    session_id = event.get("session_id")
    event_name = event.get("hook_event_name")
    turn_id = event.get("turn_id")
    if not all(isinstance(value, str) and value for value in (cwd_raw, session_id, event_name)):
        return

    marker = state_path(Path(cwd_raw))
    if not marker.exists():
        return
    state = load_state(marker)
    if not state.get("active"):
        return

    bound_session = state.get("session_id")
    if bound_session is None:
        state["session_id"] = session_id
    elif bound_session != session_id:
        return

    event_key = f"{event_name}:{turn_id or 'unknown'}"
    seen = list(state.get("seen_events") or [])
    if event_key in seen:
        return

    text: str | None = None
    block: str | None = None
    if event_name == "UserPromptSubmit":
        prompt = event.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            text = prompt
            block = callout("quote", "YOU", prompt)
    elif event_name == "Stop":
        message = event.get("last_assistant_message")
        if isinstance(message, str) and message.strip():
            text = message
            block = callout("abstract", "CODEX", message)

    if text is None or block is None:
        return
    append_markdown(Path(state["log_path"]), block)
    seen.append(event_key)
    state["seen_events"] = seen[-500:]
    save_state(marker, state)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if isinstance(payload, dict):
            handle(payload)
    except Exception as exc:  # Logging must never block the Codex turn.
        print(f"learn-codex logging warning: {exc}", file=sys.stderr)
    hook_response()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
