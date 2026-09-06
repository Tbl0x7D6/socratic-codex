#!/usr/bin/env python3
"""Create and manage opt-in Markdown learning-session logs."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_DIRNAME = ".socratic-codex"
STATE_FILENAME = "session.json"
NOTES_DIRNAME = "learning-notes"
STATE_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    chars: list[str] = []
    for char in normalized:
        if char.isalnum():
            chars.append(char)
        elif char.isspace() or char in {"-", "_"}:
            chars.append("-")
    slug = re.sub(r"-+", "-", "".join(chars)).strip("-")
    return (slug or "lesson")[:64].rstrip("-") or "lesson"


def state_path(cwd: Path) -> Path:
    return cwd.resolve() / STATE_DIRNAME / STATE_FILENAME


def load_state(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or payload.get("version") != STATE_VERSION:
        raise ValueError(f"Unsupported learning-session state: {path}")
    return payload


def save_state(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def append_markdown(path: Path, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_gap = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8") as handle:
        if needs_gap:
            handle.write("\n\n")
        handle.write(block.rstrip() + "\n")


def start_session(cwd: Path, topic: str, log: Path | None, force: bool) -> dict[str, Any]:
    cwd = cwd.resolve()
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic must not be empty.")
    marker = state_path(cwd)
    if marker.exists():
        existing = load_state(marker)
        if existing.get("active") and not force:
            raise FileExistsError(
                f"An active learning session already exists at {marker}. "
                "Stop it first or pass --force only when replacement is intended."
            )

    if log is None:
        log_path = cwd / NOTES_DIRNAME / f"{slugify(topic)}-{timestamp()}.md"
    else:
        requested_log = log.expanduser()
        log_path = (requested_log if requested_log.is_absolute() else cwd / requested_log).resolve()
    payload: dict[str, Any] = {
        "version": STATE_VERSION,
        "active": True,
        "topic": topic,
        "cwd": str(cwd),
        "log_path": str(log_path),
        "session_id": None,
        "started_at": utc_now(),
        "seen_events": [],
    }
    save_state(marker, payload)
    append_markdown(
        log_path,
        "\n".join(
            [
                f"# Learning: {topic}",
                "",
                f"Started: {payload['started_at']}",
                "",
                "> This note records user prompts and final Codex messages after logging was enabled.",
            ]
        ),
    )
    return {"state_path": str(marker), **payload}


def stop_session(cwd: Path) -> dict[str, Any]:
    marker = state_path(cwd)
    if not marker.exists():
        raise FileNotFoundError(f"No learning-session state found at {marker}")
    payload = load_state(marker)
    payload["active"] = False
    payload["stopped_at"] = utc_now()
    save_state(marker, payload)
    return {"state_path": str(marker), **payload}


def status_session(cwd: Path) -> dict[str, Any]:
    marker = state_path(cwd)
    if not marker.exists():
        return {"active": False, "state_path": str(marker), "message": "No session state found."}
    return {"state_path": str(marker), **load_state(marker)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Start an opt-in learning log")
    start.add_argument("--topic", required=True)
    start.add_argument("--cwd", type=Path, default=Path.cwd())
    start.add_argument("--log", type=Path)
    start.add_argument("--force", action="store_true")

    status = subparsers.add_parser("status", help="Show learning-log state")
    status.add_argument("--cwd", type=Path, default=Path.cwd())

    stop = subparsers.add_parser("stop", help="Stop the active learning log")
    stop.add_argument("--cwd", type=Path, default=Path.cwd())
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "start":
            result = start_session(args.cwd, args.topic, args.log, args.force)
        elif args.command == "stop":
            result = stop_session(args.cwd)
        else:
            result = status_session(args.cwd)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
