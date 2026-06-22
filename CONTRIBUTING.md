# Contributing to banana18

Thanks for helping make `banana` more practical, measurable, and useful to builders.

This project is an 18-month public build: a local AI coding assistant that grows into an Agent Evaluation & Reliability Platform. Contributions should improve the roadmap, the codebase, the measurements, or the documentation without weakening the project's main rule:

> Every meaningful deliverable should be measurable by QUALITY, COST, and LATENCY.

## What Contributions Fit

Good contributions include:

- clearer lesson plans or roadmap corrections
- stronger evaluation examples
- reproducible experiments
- runnable local examples
- tests that catch regressions
- fixes for broken links, stale instructions, or incorrect claims
- production AI lessons backed by concrete evidence
- safety, reliability, observability, or cost improvements

Please avoid vague "AI best practice" advice unless it is tied to a runnable example, a measured result, or a specific roadmap problem.

## Roadmap Alignment

`banana` is built as a dependency chain. Each month extends the previous month's work, so contributions should say which part of the roadmap they affect.

When opening an issue or PR, mention one of:

- Month 0 / prerequisites
- Month 1 client
- Month 2 evaluation
- Month 3 agent
- a later roadmap phase
- cross-cutting docs, safety, testing, or infrastructure

Large roadmap changes should explain what downstream months they affect.

## Measurement Standard

For code, experiments, evals, routing, reliability, or performance changes, include the relevant numbers:

- QUALITY: pass rate, eval score, judge agreement, reliability rate, or failure reduction
- COST: token cost, compute cost, runtime cost, manual effort, or storage impact
- LATENCY: p50/p95 time, time-to-first-token, total runtime, or CI runtime

If a change cannot yet be measured, say why and describe what measurement should be added later.

## Development Setup

This is a Python project requiring Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run tests before opening a pull request:

```bash
pytest
```

No formatter or linter is currently enforced. Keep formatting simple, readable, and consistent with nearby files.

## Pull Request Process

1. Keep PRs focused.
2. Open an issue first for large roadmap, architecture, or behavior changes.
3. Explain the problem, the tradeoff, and the affected roadmap month.
4. Add or update tests when behavior changes.
5. Update docs when commands, APIs, examples, or roadmap assumptions change.
6. Include measurement results when the change affects quality, cost, latency, reliability, or safety.
7. Be honest about limits and regressions.

A good PR description answers:

- What changed?
- Why does it matter?
- What did you run?
- What numbers changed?
- What could still be wrong?

## Documentation Style

Write plainly. Favor operational detail over motivational language.

When documenting a technique, include:

- when to use it
- when not to use it
- what can go wrong
- how to measure whether it helped
- links to runnable examples or artifacts when possible

The project values field notes with real evidence over generic tutorials.

## AI-Assisted Contributions

AI-assisted code or documentation is welcome, but contributors are responsible for the final result.

Before submitting AI-assisted work:

- verify commands and links
- remove unsupported claims
- check that examples actually run
- disclose uncertainty where the result is not proven
- avoid adding fake benchmarks, fake citations, or unverifiable numbers

## Security and Safety

Do not commit secrets, API keys, tokens, private traces, or personal data.

For agent, shell, MCP, tool-use, or prompt-injection related changes, describe the safety boundary being changed and how it was tested.

## Community

For discussion, roadmap feedback, or following the public build, join the GitHub Discussions linked in the README.
