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

## Chat-native graded question

Codex may not have a blocking quiz popup on every surface. Use the conversation itself:

```text
Question

A. Bare claim
B. Parallel bare claim
C. Parallel bare claim
D. Parallel bare claim
E. I don't know

Reply with the letter and, if useful, one sentence about your reasoning.
```

Then end the turn and wait. Do not include the correct answer, explanation, asymmetric emphasis, or a hint before the user answers.

At the beginning of the next turn:

1. Show `✓` for correct, `✗` for incorrect, or `—` for “I don't know.”
2. State the correct claim.
3. Explain the dependency that makes it correct.
4. Use the chosen distractor or note as evidence about the learner's current model.
5. Continue with the next adaptive probe or teaching node.

For multi-select questions, say explicitly that the answer is an exact set and allow `I don't know` as a separate response.

## Construct useful options

Build answer choices by construction rather than polishing them afterward:

1. Write the correct answer as a bare claim with no justification.
2. Mutate the same grammatical skeleton into each distractor.
3. Make every distractor represent a specific, plausible misconception or adjacent concept.
4. Keep options similar in length, specificity, register, and formatting.
5. Ensure each distractor is unambiguously wrong under the stated reading.

Put reasoning in the post-answer explanation, never in one privileged option. Avoid “all of the above” unless order is genuinely part of the concept.

## Vary the checks

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
