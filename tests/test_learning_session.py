from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "learning_session.py"
HOOK = ROOT / "hooks" / "learning_log.py"


def load_module():
    spec = importlib.util.spec_from_file_location("learning_session", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LearningSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.cwd = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_hook(self, payload: dict) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "PLUGIN_ROOT": str(ROOT)}
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

    def test_start_supports_unicode_topic(self) -> None:
        result = self.module.start_session(self.cwd, "神经网络 基础", None, False)
        log_path = Path(result["log_path"])
        self.assertTrue(log_path.exists())
        self.assertIn("神经网络-基础", log_path.name)
        self.assertTrue(Path(result["state_path"]).exists())

    def test_relative_log_is_resolved_from_requested_cwd(self) -> None:
        result = self.module.start_session(
            self.cwd, "Operating systems", Path("notes/os.md"), False
        )
        self.assertEqual(Path(result["log_path"]), self.cwd.resolve() / "notes" / "os.md")

    def test_empty_topic_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.module.start_session(self.cwd, "   ", None, False)

    def test_hook_binds_session_and_deduplicates_turns(self) -> None:
        result = self.module.start_session(self.cwd, "TCP reliability", None, False)
        stop_event = {
            "cwd": str(self.cwd),
            "session_id": "session-1",
            "turn_id": "turn-1",
            "hook_event_name": "Stop",
            "last_assistant_message": "Packets can be lost; reliability must add recovery.",
        }
        first = self.run_hook(stop_event)
        second = self.run_hook(stop_event)
        self.assertEqual(json.loads(first.stdout)["continue"], True)
        self.assertEqual(json.loads(second.stdout)["continue"], True)

        prompt_event = {
            "cwd": str(self.cwd),
            "session_id": "session-1",
            "turn_id": "turn-2",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "So sequence numbers identify missing data?",
        }
        self.run_hook(prompt_event)

        text = Path(result["log_path"]).read_text(encoding="utf-8")
        self.assertEqual(text.count("Packets can be lost"), 1)
        self.assertIn("So sequence numbers", text)
        state = self.module.load_state(Path(result["state_path"]))
        self.assertEqual(state["session_id"], "session-1")

    def test_other_session_cannot_append(self) -> None:
        result = self.module.start_session(self.cwd, "Compilers", None, False)
        self.run_hook(
            {
                "cwd": str(self.cwd),
                "session_id": "owner",
                "turn_id": "turn-1",
                "hook_event_name": "Stop",
                "last_assistant_message": "Owner message",
            }
        )
        self.run_hook(
            {
                "cwd": str(self.cwd),
                "session_id": "other",
                "turn_id": "turn-2",
                "hook_event_name": "Stop",
                "last_assistant_message": "Other message",
            }
        )
        text = Path(result["log_path"]).read_text(encoding="utf-8")
        self.assertIn("Owner message", text)
        self.assertNotIn("Other message", text)


if __name__ == "__main__":
    unittest.main()
