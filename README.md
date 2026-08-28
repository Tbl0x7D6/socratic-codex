# Learn for Codex

An adaptive, foundation-first learning workflow migrated from the pi-oriented
[`amosblomqvist/learn`](https://github.com/amosblomqvist/learn) project to native Codex capabilities.

Learn turns one Codex task into a guided lesson:

- diagnoses the edge of what you already understand;
- builds a compact dependency path from accepted foundations to your goal;
- alternates motivated explanation, Socratic discovery, and retrieval checks;
- uses Codex web research, subagents, and Visualize when they materially help;
- optionally mirrors the learning conversation into Markdown with native hooks.

## Use

Install the personal plugin, then start a new Codex task:

```bash
codex plugin add learn-codex@personal
```

Invoke the skill explicitly for the most predictable experience:

```text
$learn Teach me why TCP needs sequence numbers. Use Guided mode.
```

The skill can also activate implicitly for clear learning requests. It does not
replace ordinary factual answers or routine code explanations.

## Session depth

- **Quick** gives a short foundation-to-conclusion explanation.
- **Guided** diagnoses relevant prerequisites and teaches interactively.
- **Deep** maps a broader frontier, verifies the field, and uses transfer checks.

Questions are chat-native so the workflow works across Codex surfaces. The
answer and explanation appear only after you respond.

## Optional Markdown notes

Ask Learn to save notes. It will create an opt-in state marker under
`.learn-codex/` and a Markdown note under `learning-notes/`. The bundled hooks
append only user prompts and final assistant messages; ordinary Codex tasks are
untouched.

Plugin hooks require a one-time trust review. Open `/hooks`, inspect the two
Learn hooks, and trust them if you want automatic mirroring. Without trusted
hooks, the teaching workflow still works normally.

## Development

Validate the skill, plugin, and tests:

```bash
python3 /Users/be/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/learn
python3 /Users/be/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -m unittest discover -s tests -v
```

After local edits, update the cachebuster and reinstall from the personal
marketplace before testing in a new task.
