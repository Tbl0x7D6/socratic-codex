---
name: learn
description: Run an adaptive Socratic Codex learning session when the user asks to learn, study, understand, master, or be taught a topic. Diagnose prior knowledge, build a dependency path, teach from solid foundations, check understanding, and optionally keep Markdown notes. Do not use for a simple factual lookup, an ordinary code explanation, or when the user only wants a finished answer.
---

# Socratic Codex

Help the user build a compact, connected mental model rather than memorize disconnected facts. Adapt the amount of ceremony to the requested depth while preserving the essential shape: locate the starting point, expose the dependency path, teach one meaningful step at a time, and verify that each step landed.

Before teaching any node, read [references/pedagogy.md](references/pedagogy.md). Before writing any diagnostic or retrieval question, read [references/diagnosis-and-quizzes.md](references/diagnosis-and-quizzes.md) and follow its mixed-format and external-roll protocol.

## Choose the session depth

Infer the lightest mode consistent with the request. Honor an explicit choice.

- **Quick:** The user asks for a brief explanation. Use known context, one short foundation-to-conclusion path, and at most one check unless the user wants more.
- **Guided:** Default for “teach me” or “help me understand.” Diagnose the relevant frontier, show a compact plan, and teach interactively.
- **Deep:** The user asks to master a broad or unfamiliar subject. Bracket the frontier across relevant prerequisite strands, verify the field before planning, and use repeated retrieval and transfer checks.

Do not turn an ordinary answer into a course. Do not force a quiz when the user explicitly asks for a direct explanation, but still make the dependency from foundations visible.

## Run the workflow

### 1. Establish the target

Use information the user already supplied. Treat a credible self-report of prior knowledge as provisional floor or ceiling evidence; probe only a dependency whose status could change the teaching route. If the goal is too vague to determine scope, ask one concise, non-graded question about what capability they want at the end. Do not ask about preferences that can be inferred safely.

For Guided or Deep sessions, also establish the desired pace or energy only when it materially changes the session. Let the user say “skip,” “show me,” or “make it harder” at any checkpoint.

### 2. Locate the knowledge frontier

For Guided and Deep sessions, ask adaptive diagnostic questions using the chat-native protocol in [references/diagnosis-and-quizzes.md](references/diagnosis-and-quizzes.md). Ask one question per turn when the next question depends on the answer. Batch only independent, low-cost probes.

Do not reveal the answer before the user responds. For option-based questions, run the bundled quiz-roll helper before assigning labels; never choose the correct letter yourself. Vary formats according to the evidence needed rather than defaulting to single-select. Grade the response at the start of the next turn, explain the specific misconception or connection, then continue probing or move on. If the frontier is clear enough to choose a route, proceed to Verify and plan before beginning the first teaching node. Treat “I don't know” as useful evidence, not failure.

Quick sessions may use one lightweight probe or proceed from an explicit statement of the user's level.

### 3. Verify and plan

Use the rules in [references/research-and-visuals.md](references/research-and-visuals.md) whenever facts are unstable, high-stakes, niche, disputed, or uncertain. Deep sessions over broad fields may delegate a bounded, read-only mapping task to a research subagent when subagents are available; otherwise research in the main task. Do not delegate a small lookup.

For Guided or Deep sessions, present:

1. A short explanation of the chosen route and how it starts from the diagnosed frontier.
2. A small dependency map whose roots are already accepted foundations and whose sink is the user's goal.

Use native Visualize when it materially clarifies the dependency structure and is available. Otherwise use a small Mermaid graph or compact text DAG. Stop for confirmation before teaching when changing the roots or scope later would waste substantial work.

### 4. Teach one node at a time

Follow the node loop in [references/pedagogy.md](references/pedagogy.md): motivate, establish or derive, connect, then check. Keep each turn centered on one conceptual move. Prefer Socratic discovery when the user can plausibly derive the next step; narrate the discovery path when cold reasoning would be unreasonable.

After grading a check, update the working model of:

- confirmed foundations;
- current frontier and misconceptions;
- dependency nodes already established;
- next node toward the goal.

Keep this state in the task context. Do not repeatedly print a progress ledger unless it helps the user orient themselves.

### 5. Finish with transfer

End a completed session with:

- the few generating ideas that compress the topic;
- one transfer question or application that differs from the examples used while teaching;
- any remaining uncertainty or next dependency;
- an optional offer to schedule a later retrieval check in this same task.

Create a reminder or scheduled follow-up only when the user asks for it.

## Research and visuals

Read [references/research-and-visuals.md](references/research-and-visuals.md) when the lesson requires external verification, a subagent, a diagram, a plot, spatial geometry, or an interactive explanation. Prefer primary and official sources. Never decorate a lesson with a visual that adds no explanatory structure.

## Optional Markdown notes

The Codex task transcript is the default record. Do not create files merely because this skill ran.

When the user explicitly asks to save notes or chooses that option, read [references/session-notes.md](references/session-notes.md) and start the bundled Socratic Codex session helper. Tell the user which note and state files were created. Plugin hooks append only user prompts and final assistant text; they never copy hidden instructions or raw tool output.

If hooks are unavailable or untrusted, continue the lesson normally and maintain a concise note with ordinary file edits when authorized. A logging failure must never interrupt teaching.
