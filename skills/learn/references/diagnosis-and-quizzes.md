# Diagnosis and quiz protocol

Use diagnosis to locate the learner's frontier, not to perform or intimidate. Every question should change the next teaching decision.

## Bracket the frontier

For each prerequisite strand relevant to the goal, seek both:

- a **floor**: something the learner can answer or explain reliably;
- a **ceiling**: the first point they cannot yet answer, or answer using a misconception.

The frontier lies between them.

When an answer is correct, increase difficulty enough to gain information. When it is wrong, probe nearby before concluding whether it is a slip, isolated gap, vocabulary problem, or systematic model error. Treat a credible self-report as provisional evidence and verify it only when the result would change the route. In Deep mode, bracket every strand the lesson will actually use. In Guided mode, stop once the plan can be chosen confidently; then proceed to Verify and plan before beginning the first teaching node.

## Distinguish two kinds of question

Use a preference question only when no answer is objectively correct, such as the desired application, pace, or direction.

Use a graded question when there is a definite answer, including Socratic discovery prompts. Never hide a factual quiz inside a “preference” question.

## Choose a question format

Match the format to the evidence needed. Prefer a response the learner must generate when that is affordable; recognition alone is weak evidence of mastery.

- **Single-select:** discriminate among nearby models or locate a misconception efficiently.
- **Multi-select:** identify an exact set of conditions, properties, causes, or consequences.
- **Short answer or fill-in:** retrieve a term, invariant, relationship, or intermediate result without cues.
- **Prediction:** commit to an output, direction, or state change before seeing the explanation.
- **Ordering:** arrange causal, procedural, temporal, or derivation steps.
- **Matching or classification:** map examples to concepts, mechanisms, or categories.
- **Error diagnosis and repair:** find the faulty step and correct it.
- **Explain-back:** justify a dependency or teach the node in the learner's own words.
- **Worked application:** calculate, derive, code, debug, or apply the node to a fresh case.
- **Transfer:** solve a structurally similar problem whose surface details differ from the lesson.

True/false is acceptable only when the learner must also repair a false statement or justify a true one. Otherwise it provides too little diagnostic information.

Do not use single-select twice in succession when another format can test the same dependency at comparable cost. After a recognition check, use a generative, application, or transfer check before treating the node as mastered. In a sufficiently long Guided or Deep session, sample at least three formats; do not prolong a lesson merely to satisfy that variety.

When two or more formats are equally suitable, the format itself may be selected outside the model. First list only pedagogically valid candidates, then run:

```bash
python3 <plugin-root>/scripts/quiz_roll.py choose prediction short-answer ordering
```

Use the returned `selected` format. Never put an unsuitable format into the pool merely for novelty.

## Roll answer positions before rendering choices

For every single-select or multi-select question, determine the semantic answer and distractors before assigning letters. Then use the bundled helper to roll the answer position immediately before rendering the question. Resolve `<plugin-root>` as two directories above this skill directory.

Single-select with four options:

```bash
python3 <plugin-root>/scripts/quiz_roll.py positions --options 4 --correct 1
```

Multi-select with five options and two correct claims:

```bash
python3 <plugin-root>/scripts/quiz_roll.py positions --options 5 --correct 2
```

Place the correct claim or claims at exactly the returned `correct_positions`; fill every other position with a distractor. Do not manually choose a favored letter, move an answer after the roll, or expose the roll output or answer key before the learner responds. If the command cannot be run, do not pretend the position is random: switch to a non-option format.

## Chat-native graded question

Codex may not have a blocking quiz popup on every surface. Use the conversation itself:

```text
Single-select

A. Bare claim
B. Parallel bare claim
C. Parallel bare claim
D. Parallel bare claim
E. I don't know

Reply with the letter and, if useful, one sentence about your reasoning.
```

Then end the turn and wait. Do not include the correct answer, explanation, asymmetric emphasis, or a hint before the user answers.

At the beginning of the next turn:

1. Show `✓` for correct, `✗` for incorrect, `△` for meaningfully partial, or `—` for “I don't know.”
2. State the correct claim.
3. Explain the dependency that makes it correct.
4. Use the chosen distractor or note as evidence about the learner's current model.
5. Continue with the next adaptive probe or teaching node.

State a compact response contract for every format: for example, one letter; an exact letter set such as `A,C`; an order such as `C→A→B`; mappings such as `1-B, 2-C`; or at most two sentences. Always allow `I don't know` as a separate response.

Before asking an open-response question, privately establish the minimum correct elements and which omissions count as partial rather than incorrect. Do not reveal that rubric. Grade the meaning, not exact wording, and call out ambiguity in the question instead of penalizing the learner for it.

## Construct useful options

Build answer choices by construction rather than polishing them afterward:

1. Write the correct answer as a bare claim with no justification.
2. Mutate the same grammatical skeleton into each distractor.
3. Make every distractor represent a specific, plausible misconception or adjacent concept.
4. Keep options similar in length, specificity, register, and formatting.
5. Ensure each distractor is unambiguously wrong under the stated reading.

Put reasoning in the post-answer explanation, never in one privileged option. Avoid “all of the above” unless order is genuinely part of the concept.

## Vary the cognitive work

Use the cheapest check that can expose the relevant dependency:

- retrieval: identify a definition or invariant;
- prediction: say what changes when an input changes;
- explanation: justify why a result must follow;
- discrimination: distinguish nearby concepts;
- application: use the node in a new example;
- transfer: solve a structurally similar problem in a different surface form.

Do not confuse repeated recognition questions with mastery. A completed Guided or Deep session should include at least one transfer check unless the user ends early.

## Respect the learner

- “I don't know” is high-quality information and is never marked wrong in tone.
- Let the user skip, request the answer, reduce intensity, or switch to exposition.
- Do not continue binary-search probing after the teaching path is already clear.
- Never manufacture a knowledge deficit to justify a longer lesson.
