from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "quiz_roll.py"


def load_module():
    spec = importlib.util.spec_from_file_location("quiz_roll", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class QuizRollTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_single_answer_position_is_valid(self) -> None:
        result = self.module.roll_positions(4, 1, random.Random(11))
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], {"A", "B", "C", "D"})

    def test_multiple_answer_positions_are_unique_and_sorted(self) -> None:
        result = self.module.roll_positions(6, 3, random.Random(3))
        self.assertEqual(result, sorted(set(result)))
        self.assertEqual(len(result), 3)
        self.assertTrue(set(result) <= set("ABCDEF"))

    def test_invalid_position_request_is_rejected(self) -> None:
        for option_count, correct_count in ((1, 1), (4, 0), (4, 4), (27, 1)):
            with self.subTest(option_count=option_count, correct_count=correct_count):
                with self.assertRaises(ValueError):
                    self.module.roll_positions(option_count, correct_count)

    def test_choose_requires_unique_candidates(self) -> None:
        with self.assertRaises(ValueError):
            self.module.roll_item(["prediction"])
        with self.assertRaises(ValueError):
            self.module.roll_item(["prediction", "prediction"])

    def test_cli_emits_machine_readable_roll(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "positions",
                "--options",
                "5",
                "--correct",
                "2",
            ],
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["mode"], "positions")
        self.assertEqual(len(payload["correct_positions"]), 2)
        self.assertRegex(payload["roll_id"], r"^[0-9a-f]{8}$")


if __name__ == "__main__":
    unittest.main()
