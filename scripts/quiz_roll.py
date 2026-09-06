#!/usr/bin/env python3
"""Make quiz layout choices outside the language model."""

from __future__ import annotations

import argparse
import json
import random
import secrets
from collections.abc import Sequence
from typing import Any


MAX_OPTIONS = 26


def roll_positions(
    option_count: int,
    correct_count: int,
    rng: random.Random | random.SystemRandom | None = None,
) -> list[str]:
    """Return sorted, unique letter slots for the answer key."""
    if not 2 <= option_count <= MAX_OPTIONS:
        raise ValueError(f"option_count must be between 2 and {MAX_OPTIONS}")
    if not 1 <= correct_count < option_count:
        raise ValueError("correct_count must be at least 1 and less than option_count")
    chooser = rng or random.SystemRandom()
    indexes = sorted(chooser.sample(range(option_count), correct_count))
    return [chr(ord("A") + index) for index in indexes]


def roll_item(
    items: Sequence[str],
    rng: random.Random | random.SystemRandom | None = None,
) -> str:
    """Choose one non-empty item from a caller-vetted candidate set."""
    cleaned = [item.strip() for item in items if item.strip()]
    if len(cleaned) < 2:
        raise ValueError("provide at least two non-empty candidates")
    if len(set(cleaned)) != len(cleaned):
        raise ValueError("candidates must be unique")
    chooser = rng or random.SystemRandom()
    return chooser.choice(cleaned)


def emit(payload: dict[str, Any]) -> None:
    payload["roll_id"] = secrets.token_hex(4)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Roll quiz positions or choose among pre-vetted question formats."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    positions = subparsers.add_parser(
        "positions", help="Roll one or more correct answer positions"
    )
    positions.add_argument("--options", type=int, required=True)
    positions.add_argument("--correct", type=int, default=1)

    choose = subparsers.add_parser(
        "choose", help="Choose one item from equally suitable candidates"
    )
    choose.add_argument("candidates", nargs="+")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "positions":
            positions = roll_positions(args.options, args.correct)
            emit(
                {
                    "mode": "positions",
                    "option_count": args.options,
                    "correct_count": args.correct,
                    "correct_positions": positions,
                }
            )
        else:
            selected = roll_item(args.candidates)
            emit(
                {
                    "mode": "choose",
                    "candidates": args.candidates,
                    "selected": selected,
                }
            )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
