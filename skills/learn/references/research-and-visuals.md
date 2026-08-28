# Research and visual decisions

Read this reference only when the lesson needs external verification, delegation, or a visual artifact.

## Verify claims proportionally

Browse or use an authoritative connected source when a claim is current, high-stakes, niche, disputed, specifically cited by the user, or not recalled with high confidence. Prefer primary sources, official documentation, standards, datasets, and research papers over summaries.

Keep the research question bounded by the lesson goal. A small factual lookup belongs in the main task. For a broad Deep-mode topic, a research subagent may map independent facets such as foundations, standard framings, and common misconceptions. Give it a read-only brief, require source links, and ask for a compact synthesis rather than raw search output.

If research corrects the planned foundation or derivation, say so plainly before teaching from it.

## Decide whether a visual earns its place

Use a visual for relationships that prose carries poorly:

- dependency graphs and hierarchies;
- flows, sequences, and state transitions;
- spatial or geometric relationships;
- comparisons across several repeated fields;
- a plot whose shape is the concept;
- an interactive “what changes if” explanation.

Skip a visual that merely places a sentence inside a box.

## Prefer Codex-native visualization

When the Visualize plugin is available, invoke it for an interactive graph, diagram, simulation, plot, or practice tool. Give it one idea and the fewest elements needed. Inspect the result for false edges, wrong directions, bad scales, clipping, or unreadable labels before using it in the lesson.

If Visualize is unavailable:

- use a small Mermaid diagram for nodes and edges;
- use a compact table for repeated comparisons;
- create an SVG or static scientific figure only when exact geometry or data requires it;
- use plain text when it is clearer than an artifact.

Do not require a separate maker subagent solely to render a simple dependency map. Delegate visual work only when independent visual QA materially improves correctness.
