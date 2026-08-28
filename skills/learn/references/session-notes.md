# Optional Markdown learning notes

The task transcript is the default record. Start file logging only after the user explicitly asks to save notes or accepts an offered note workflow.

## Start logging

Resolve the plugin root as two directories above this skill directory. Run:

```bash
python3 <plugin-root>/scripts/learning_session.py start --topic "<topic>" --cwd "<current-working-directory>"
```

The helper creates:

- `<cwd>/.learn-codex/session.json`, a small active-session marker;
- `<cwd>/learning-notes/<topic>-<timestamp>.md`, the Markdown note.

Pass `--log <path>` only when the user requested a particular note file. Never use `--force` unless the user explicitly wants to replace an active marker. Report both created paths.

The plugin's `UserPromptSubmit` and `Stop` hooks bind the marker to the current Codex session, then append user prompts and final assistant messages as Markdown callouts. They do not copy system instructions, hidden context, reasoning, or raw tool output.

Plugin hooks must be reviewed and trusted by the user. If they have not been trusted, explain that `/hooks` enables automatic mirroring; continue the lesson without blocking. You may still maintain a concise note through ordinary file edits when authorized.

## Check or stop logging

```bash
python3 <plugin-root>/scripts/learning_session.py status --cwd "<current-working-directory>"
python3 <plugin-root>/scripts/learning_session.py stop --cwd "<current-working-directory>"
```

Stopping marks the session inactive but keeps the note and marker recoverable. Because the stop command runs before the turn's final `Stop` hook, append any desired final summary to the note before stopping.

## Keep notes useful

The automatic transcript is supporting evidence, not the final study artifact. At major checkpoints or completion, add a concise summary containing:

- the learning goal;
- confirmed foundations;
- the located frontier and corrected misconceptions;
- the dependency path;
- key derivations or examples;
- the transfer result and next review target.

When resuming from a note, read the summary and recent transcript, restate the inferred frontier briefly, and let the user correct it before continuing.
