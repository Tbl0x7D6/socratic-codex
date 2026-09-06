# Socratic Codex

Codex-native adaptive learning for building connected mental models instead of
memorizing isolated facts.

Migrated from the pi-oriented
[`amosblomqvist/learn`](https://github.com/amosblomqvist/learn) workflow.

## Features

- Diagnose the learner's starting point and build a dependency path.
- Teach one concept at a time with Socratic discovery or concise explanation.
- Use single-select, multi-select, short answer, prediction, ordering,
  matching, error repair, application, and transfer checks.
- Randomize option positions outside the model for option-based questions.
- Optionally save prompts and final answers as Markdown notes through hooks.

## Use

Install the plugin, then start a new Codex task:

```bash
codex plugin add socratic-codex@personal
```

Invoke the skill with its stable command name:

```text
$learn Teach me why TCP needs sequence numbers. Use Guided mode.
```

Open `/hooks` to review and trust the optional Markdown logging hooks.

## Development

The repository root is the plugin root. Run the checks from this directory:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/learn
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -m unittest discover -s tests -v
```

After source changes, refresh the local cachebuster, reinstall
`socratic-codex@personal`, and test in a new Codex task.
