# Month 03 - Your First AI Coding Agent + Context Engineering
### Applied AI Engineer Master Roadmap · Instructor's Edition (Professor's Notes)

---

> **Teaching philosophy.** For two months you've built infrastructure with no agent in it. Month 1 gave you a client that measures every call. Month 2 gave you an eval harness that scores every output and a gate that blocks regressions. Now - finally - you build the thing those tools were always meant to measure: a coding agent. But here's the trap I'm going to spend all month keeping you out of. The moment people build their first agent, they fall in love with it. They make it smarter, give it more tools, let it run longer, and six weeks later they have an impressive demo that nobody can trust because nobody measured it. You are not going to do that. Your agent is a *means*, not the prize. It's the system-under-test for the platform you're really building. So you'll keep it deliberately humble - *supervised*, meaning it proposes and you approve - and you'll point your Month 2 harness at it from the first working version. The skill this month is not "make an agent." Anyone can `pip install` a framework and call `.run()`. The skill is building the control loop yourself so you know exactly what the framework hides, getting the *right code* into the context window (which is 80% of why agents fail), and proving with a number whether your retrieval is the problem or the model is. An agent you can't measure is a slot machine. You already own the measuring tape. This month you build something worth measuring.
>
> **The one rule of this month:** *Before you build an agent for a task, ask "would a deterministic script do this?" - and before you blame the model, measure the retrieval. Most agent failures are context failures wearing a model's clothes.*

---

## Month 3 Learning Outcomes (what you must be able to DO by Day 30)

By the end of this month, without notes, you can:

1. **BUILD** - a supervised coding agent inside `banana`: it retrieves relevant code, proposes an edit as a diff, waits for your approval, runs the tests, and reports the result - all on a bounded control loop with hard step/token/time limits.
2. **BUILD** - the agent control loop from scratch (observe → decide → act → repeat) in under 60 lines *before* you touch a framework, so you can reason about what LangGraph or the OpenAI Agents SDK hides.
3. **BUILD** - a code-aware retrieval pipeline: tree-sitter chunking + hybrid (BM25 + vector) search + reranking, following Anthropic's Contextual Retrieval recipe rather than naive vector search.
4. **MEASURE** - retrieval quality *independently* of generation: `recall@k` for "did the retriever surface the files this change actually touches?", and the measured lift of hybrid+rerank over vector-only.
5. **MEASURE** - the agent on your Month 2 golden set through the existing harness: task-completion %, tool-call accuracy, and diff-accept rate - plus steps-to-completion and the local-vs-cloud cost gap.
6. **BREAK** - induce and diagnose the agent's real failure modes: an unbounded loop, a tool timeout, a malformed/hallucinated diff, and context rot from a stuffed window - and show your guards catch each.
7. **DEFEND** - explain from memory why retrieval is measured separately from generation, when a workflow beats an agent, and the honest point where your local agent loses to a frontier API.

> **Assessment is behavioral.** Each week ends with a pass/fail checkpoint. The month ends with a recorded ~10-minute oral defense: demo the supervised loop live (propose → approve → test → report), show the agent scored by the Month 2 harness, whiteboard the control loop from memory, prove your retrieval lift with `recall@k`, and state honestly where the agent breaks. If you can't run it on camera and defend the numbers, it isn't done.

---

## The Mental Model / "Spine"

Pin this. Everything in Month 3 hangs off it:

> **An agent is a `while` loop around an LLM call, with tools as its only way to touch the world and the context window as its only memory.** The loop observes state, asks the model to decide, executes a tool, feeds the result back, and repeats until done or until a hard limit stops it. Two things decide whether it works: the quality of what you put *in* the window (retrieval) and the discipline of what you let *out* of the loop (tools, limits, approval). The model is the smallest variable. Master the loop and the context, and the model becomes swappable.

**Connection to prior months' spines:** Month 1 - "a model call is a flaky, metered, non-deterministic upstream service." Month 2 - "an eval harness is a test suite for non-deterministic software." Month 3 wraps that flaky call in a loop and points the harness at the loop. The agent *is* a sequence of Month 1 calls; the harness that scored one call now scores the whole sequence. You're not building something new - you're composing the two things you already have.

**Connection forward:** Month 4 stops scoring just the final diff and starts scoring the *trajectory* - was the plan sensible, were the tool calls efficient, did it edit the right files? Your trajectory logs this month are the raw material for that. Month 5 turns this single agent into a multi-agent system, benchmarked against this month's single-agent baseline on the same task suite - so the numbers you record now are the bar everything later must beat. Month 7 makes the tools speak MCP so any agent can use them. Build the loop and the tools cleanly now, and the rest of Phase 2 is extension, not rework.

---

# WEEK 1 - "The loop and the tools": the control loop and tool design as API design

**Theme:** An agent is not magic - it's a loop and a set of functions it's allowed to call. This week you build the loop yourself (no framework), design tools the way you'd design a typed REST API, and put a hard cap on the loop so it can never run away. By Friday you have a read-only agent that can reason about a codebase and tell you what it *would* do - without changing anything yet.

---

### Concept block (~2h)

| Session | Source | What to EXTRACT (a purpose to read for, never "finish") |
|---|---|---|
| 1.1 (45m) | **Anthropic - "Building Effective Agents"** | The core distinction: a *workflow* is a fixed, pre-defined sequence of LLM calls; an *agent* dynamically decides its own steps. Extract the six patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and the autonomous agent). Note their thesis: *most production "agents" should be workflows.* Write down the one-line rule for when an agent is actually justified. |
| 1.2 (30m) | **Lilian Weng - "LLM-Powered Autonomous Agents"** | Extract the anatomy: planning, memory, tool use, and the action loop. Focus on ReAct (reason + act interleaved). Don't memorize the survey - extract the *loop shape* you're about to implement: thought → action → observation → repeat. |
| 1.3 (30m) | **Chip Huyen - *AI Engineering*, "Agents" chapter** | Extract: tool design as the agent's API surface; the failure modes of tool use (wrong tool, wrong args, no stopping); and *why bounding the loop matters*. Anchor it to your world: a tool call is an RPC the model issues, and an unbounded agent is a retry loop with no max-attempts. |
| 1.4 (15m) | **OpenAI Agents SDK + LangGraph docs (skim only)** | Do NOT adopt either yet. Extract the shared vocabulary - "tools," "state," "nodes/steps," "handoffs," the run loop. You're reading these so that when you build the loop by hand next, you can point at each abstraction and say "I wrote that part myself." |

> **Professor's Note - tools are an API contract, and you already know how to design those.** Stop thinking of a tool as "a function the AI calls" and start thinking of it as a public endpoint with an untrusted, occasionally-drunk client. The model will pass malformed arguments, call `read_file` on paths that don't exist, and invent parameters. So you design tools exactly as you'd design a REST API for a flaky integration: typed inputs, validated arguments, a *structured error* return instead of a thrown exception (the model needs to read the error and recover, not crash the loop), and - critically - idempotency where you can get it. `read_file` and `grep` are safe to retry. `propose_edit` is not idempotent (it mutates a draft), so it gets approval gating. This is the same `GET`-vs-`POST` reasoning from Month 1's "an LLM call is non-idempotent." You're not learning a new skill. You're applying API design to a new kind of caller.

---

### Lab 1 - BUILD: tools as a typed API (~2.5h)

**Goal:** Four typed, validated, individually-testable tools that are the agent's only way to touch the codebase. No agent yet - just the tools and their tests.

**Steps:**

1. **Create the agent package** inside `src/banana` (extending the Month 2 layout):
   ```
   src/
   └── banana/
       ├── clients/         # Month 1
       ├── evaluation/      # Month 2
       └── agents/
           ├── __init__.py
           ├── tools.py     # This lab
           ├── loop.py      # Lab 2
           ├── retrieval.py  # Week 2
           ├── supervisor.py # Week 3 (approval + diff apply)
           └── trajectory.py # Week 3 (logging)
   ```

2. **Define a `ToolResult` contract** - every tool returns the same shape so the loop can treat them uniformly:
   ```python
   @dataclass
   class ToolResult:
       ok: bool
       content: str            # what the model sees next turn
       error: str | None = None
       meta: dict = field(default_factory=dict)   # latency_ms, bytes, n_matches...
   ```

3. **Implement four tools**, each `(args) -> ToolResult`, each validating its own input and *returning* errors rather than raising:
   - `read_file(path: str, max_bytes: int = 20_000)` - refuse paths outside the repo root (path-traversal guard); truncate large files and say so.
   - `grep(pattern: str, path_glob: str = "**/*.py")` - wraps `ripgrep`/`re`; cap results (e.g., 50 matches) so the model can't flood its own context.
   - `list_dir(path: str)` - directory listing, repo-root-bounded.
   - `run_tests(test_path: str, timeout_s: int = 30)` - runs `pytest` in a subprocess with a **timeout**; returns pass/fail counts and the tail of stdout. (Reused directly from your Month 2 `test_check` instinct.)

4. **Write the tool schema** the model will see - a JSON description of each tool's name, purpose, and typed parameters. This is the agent's API documentation, written for a machine reader.

5. **Unit-test every tool with `pytest`** - including the *bad* paths: a non-existent file, a traversal attempt (`../../etc/passwd`), a `grep` that matches 10,000 lines (does the cap hold?), a `run_tests` that hangs (does the timeout fire?).

**ACCEPTANCE:** `pytest tests/test_agent_tools.py` is green, including the abuse cases. Every tool returns `ToolResult` - no tool raises on bad input. The path-traversal guard and the `run_tests` timeout are both proven by a test.

**Target number:** 4 tools, 100% returning structured errors on bad input (0 uncaught exceptions across the abuse suite).

---

### Lab 2 - BUILD: the bounded control loop from scratch (~3h)

**Goal:** A working observe → decide → act loop that uses your tools, runs entirely on your local Qwen, and *cannot* run away. Read-only for now (no editing).

**Steps:**

1. **Write the loop in `src/banana/agents/loop.py`** - no framework. The shape:
   ```python
   def run_agent(task: str, tools: dict, *, max_steps=8, max_tokens=8000,
                 wall_clock_s=120) -> AgentRun:
       messages = [system_prompt(tools), user(task)]
       for step in range(max_steps):
           # DECIDE: ask the model for the next action (tool + args) as JSON
           resp = client.generate(messages, ...)          # Month 1 client
           action = parse_action(resp.text)               # tool name + args, or "final"
           if action.is_final:
               return AgentRun(done=True, answer=action.text, steps=step, ...)
           # ACT: execute the tool
           result = tools[action.name](**action.args)     # returns ToolResult
           # OBSERVE: feed the result back in
           messages.append(assistant(resp.text))
           messages.append(tool_result(action.name, result.content))
           if over_budget(tokens, time): break
       return AgentRun(done=False, reason="hit limit", steps=max_steps, ...)
   ```

2. **Design the system prompt** that teaches the model the loop: "You have these tools. Respond with exactly one JSON action per turn: `{tool, args}` or `{final, answer}`. Think briefly, then act." The prompt *is* the agent's behavior - treat it like Month 2's judge prompt.

3. **Enforce three hard limits** - `max_steps`, `max_tokens` (sum across the run, using Month 1's telemetry), and `wall_clock_s`. Hitting any limit ends the run cleanly with `done=False` and a reason. **These are non-negotiable. An agent without limits is a fork bomb with good intentions.**

4. **Capture an `AgentRun`** with the full step list (each step: thought, action, tool result, latency) - this is the seed of Week 3's trajectory log and Month 4's trajectory eval.

5. **Run it read-only** on 2–3 of your Month 2 golden tasks, asking it only to *locate and explain* the bug (no editing yet). Watch it call `grep`, `read_file`, reason, and produce a final answer. Use `qwen2.5-coder:7b` via Ollama.

**ACCEPTANCE:** `python -m banana.agents.loop --task "find the off-by-one bug in task_001"` runs, makes real tool calls, and returns either a final answer or a clean limit-hit. You can read the step-by-step `AgentRun`. The loop never exceeds `max_steps`.

**Target number:** Average steps-to-answer on 3 read-only tasks, and the % of those runs that terminate by `final` vs. by hitting a limit. (Record it - this is your steps-to-completion baseline.)

---

### Lab 3 - BREAK: the runaway loop (~1h)

**Goal:** Prove your limits actually bind. An agent that *can* loop forever will, eventually, on a Saturday, while your battery dies.

**Steps:**

1. **Provoke a loop:** give the agent a task with no possible answer ("find the function `nonexistent_handler` and explain it") and watch it `grep`, find nothing, and try again. **Does it stop at `max_steps`?** Confirm the run ends with `done=False, reason="hit limit"`.

2. **Provoke a token blowout:** point it at a task and set `read_file`'s cap absurdly high so one file floods the window. **Does `max_tokens` trip before the context overflows?** If the model errors on an oversized context instead of your guard firing first, your guard is in the wrong place - move it.

3. **Provoke a wall-clock hang:** make `run_tests` target a test that sleeps past its timeout. **Does the per-tool timeout fire AND the run-level `wall_clock_s` hold as a backstop?** You want defense in depth: the tool times out, and even if it didn't, the loop would.

4. **Provoke a parse failure:** make the model emit malformed action JSON (lower a small model's temperature won't help - use `1.5b` at high temperature). **Does `parse_action` return a structured "I couldn't parse that" that the loop feeds back as an observation, so the model can retry - instead of crashing?**

**ACCEPTANCE:** All four runaways are stopped by a guard, and you can name *which* guard caught each. Document the four in `src/banana/agents/FAILURE_MODES.md` (this file grows all month). At least one run ends in a clean `❌ hit limit` rather than an exception.

> **Professor's Note - this is the lesson the demos skip.** Every viral agent demo shows the happy path. None show the 3 a.m. run that burned 40,000 tokens looping on a typo. The difference between a toy and a system is that the system *fails safely*: bounded steps, bounded tokens, bounded time, and parse errors fed back as observations instead of crashes. You've built circuit breakers and retry caps in distributed systems - this is the same instinct applied to a model that will, given the chance, try the same wrong thing forever. The limits aren't a nice-to-have. They're the feature.

---

### Deep-Understanding Drill - Week 1

**From-scratch exercise (~45m):** Implement a minimal ReAct loop in **under 50 lines** - no `banana.agents`, no framework. Raw HTTP to Ollama (reuse your Month 1 raw-call drill), one hardcoded tool (`grep` via `subprocess`), a `for` loop with `max_steps=5`, and a hand-written parser that pulls `{tool, args}` out of the model's text. Run it on one real question about a real file.

**Why:** LangGraph, the OpenAI Agents SDK, CrewAI - they're all this loop with a state machine, retries, and telemetry bolted on. If you can write the 50-line version, you can read any framework's docs and immediately see *which part of your loop they replaced and what they added*. When the framework does something surprising, you'll drop to this mental model and find the bug. This is the difference between configuring an agent and understanding one.

**ACCEPTANCE:** A standalone script under 50 lines that completes at least one observe→act→observe→final cycle against a real model, with a visible step trace. No imports from `banana.agents`.

---

### ✅ Week 1 Checkpoint (pass/fail)

- [ ] Four typed tools with `ToolResult` contract; all return structured errors on bad input
- [ ] Tool abuse suite green (traversal guard, result caps, `run_tests` timeout proven)
- [ ] Bounded control loop runs read-only against local Qwen, makes real tool calls
- [ ] Three hard limits (steps, tokens, wall-clock) enforced and individually proven by a BREAK
- [ ] Parse failures fed back as observations, not crashes
- [ ] Minimal ReAct loop (< 50 lines, no framework) works standalone

**Target numbers:** Steps-to-answer on 3 read-only tasks; % of runs ending in `final` vs. limit; 0 uncaught exceptions across the tool abuse suite.

---

### Socratic Questions - Week 1

1. Your loop asks the model for one JSON action per turn. The model sometimes wraps it in prose or markdown fences. **Where should you handle that - in the prompt, the parser, or both?** What's the failure mode if you only fix one?
2. You set `max_steps=8`. A genuinely hard task needs 12 steps; a runaway burns 50. **How do you tell "needs more steps" apart from "stuck in a loop" without just raising the cap?** (Hint: look at *what changes* between steps, not just the count.)
3. `read_file` and `grep` are safe to retry; `propose_edit` is not. **Which of your future tools are idempotent, and how does that change how the loop is allowed to call them?** Anchor it to `GET` vs `POST`.

---

# WEEK 2 - "Get the right code in the window": context engineering and retrieval

**Theme:** The model is rarely the bottleneck - the *context* is. This week you build a code-aware retriever (tree-sitter chunking, hybrid BM25 + vector, reranking), measure its quality *independently* of the agent with `recall@k`, and prove how much Anthropic's Contextual Retrieval recipe beats naive vector search. Then you break it by stuffing the window and watching quality fall - context rot, measured.

---

### Concept block (~2h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 2.1 (40m) | **Anthropic - "Contextual Retrieval"** | The recipe and *why each piece helps*: contextual embeddings + contextual BM25 + reranking cut retrieval failures ~67% in their tests. Extract the mechanism - prepend a short context blurb to each chunk before embedding so the chunk isn't ambiguous out of its file. This is your default, not naive vector search. |
| 2.2 (35m) | **Anthropic - "Effective Context Engineering for AI Agents"** | Extract **context rot**: model performance degrades as the window fills - you have a finite "attention budget." Fewer, better tokens beat more tokens. Extract two techniques you'll implement: compaction (summarize old turns) and external note-taking (write findings to a scratchpad outside the window). |
| 2.3 (25m) | **LangChain (Harrison Chase) - "The Rise of Context Engineering"** | Extract the reframe: prompt engineering → *context* engineering. The job is curating what's in the window at each step, not crafting one clever prompt. Note the four moves: write, select, compress, isolate. |
| 2.4 (20m) | **tree-sitter docs** | Extract how to parse source into an AST and walk it to extract *whole functions/classes* as chunks (instead of blindly splitting every 500 chars). A chunk that cuts a function in half is a poisoned chunk. You want syntactic boundaries. |

> **Professor's Note - "the model is dumb" is almost always "the context is wrong."** This is the single most expensive misdiagnosis in agent engineering, so I'm going to make you measure your way out of it. When your agent fails a task, there are two suspects: the retriever put the wrong files in the window, or the model couldn't use the right files. These have *opposite* fixes - one is an engineering problem (chunking, ranking, recall), the other is a model problem (bigger model, better prompt). If you can't tell them apart, you'll spend two weeks tuning prompts when the real bug is that the relevant file never made it into context. So you measure retrieval *separately*, with `recall@k`, before you ever blame the model. This is exactly like debugging a slow API call by measuring DB time and network time separately instead of staring at the total. Decompose, then diagnose.

---

### Lab 4 - BUILD: code-aware chunking + a hybrid retriever (~3.5h)

**Goal:** A retriever that, given a task description, returns the top-k code chunks most likely to be relevant - using syntactic chunks, hybrid search, and reranking.

**Steps:**

1. **Chunk with tree-sitter** (`src/banana/agents/retrieval.py`): parse each `.py` file, extract functions and classes as chunks with metadata (`file`, `symbol`, `start_line`, `end_line`). No chunk straddles a function boundary.

2. **Add contextual prefixes** (the Anthropic recipe): for each chunk, prepend a one-line context blurb - e.g., `"From payments/refund.py, function process_refund, part of the refund flow:"` - *before* embedding and *before* BM25 indexing. This is the "contextual" in Contextual Retrieval.

3. **Build two indexes over the same chunks:**
   - **Vector:** embed each contextualized chunk with `nomic-embed-text` (or `bge-*`) via Ollama; store vectors (a flat numpy array + cosine search is fine - no vector DB needed at this scale).
   - **BM25:** a lexical index over the contextualized chunk text (use `rank_bm25` or a small hand-rolled TF-IDF).

4. **Fuse and rerank:** for a query, take top-N from each index, merge (reciprocal rank fusion is a clean default), then **rerank** the merged set with a cross-encoder or a cheap LLM rerank pass, and return top-k.

5. **Expose one function:** `retrieve(query: str, k: int = 5) -> list[Chunk]`. The agent will call this to fill its context; you'll also call it directly to measure it.

**ACCEPTANCE:** `retrieve("fix the off-by-one in the pagination helper", k=5)` returns 5 syntactically-clean chunks with file/symbol/line metadata. You can swap between `vector_only`, `bm25_only`, and `hybrid_rerank` modes with a flag.

**Target number:** Retrieval latency p50 for `k=5` (record it - retrieval is now part of your agent's latency budget).

---

### Lab 5 - MEASURE: recall@k, vector-only vs hybrid+rerank (~2.5h)

**Goal:** Quantify retrieval quality *independently of the model*, and measure the lift from the full recipe. This number tells you whether to fix retrieval or the model.

**Steps:**

1. **Build a retrieval ground-truth set.** For each Month 2 golden task, label which file(s)/symbol(s) the known-good solution actually touches. That's the "relevant set" for that query. (You already have the solutions - this is bookkeeping, not new judgment.) Store as `src/banana/evaluation/golden/retrieval_truth.jsonl`.

2. **Define `recall@k`:** of the relevant chunks for a task, how many appear in the retriever's top-k? Average across tasks. Add `MRR` (mean reciprocal rank) if you want the position signal too.

3. **Run all three modes** - `vector_only`, `bm25_only`, `hybrid_rerank` - over every task at `k = 1, 3, 5, 10`. Produce the table:

   | Mode | recall@1 | recall@3 | recall@5 | recall@10 | p50 latency |
      |---|---|---|---|---|---|
   | vector_only | ? | ? | ? | ? | ? |
   | bm25_only | ? | ? | ? | ? | ? |
   | hybrid_rerank | ? | ? | ? | ? | ? |

4. **Compute the lift:** `hybrid_rerank` recall@5 minus `vector_only` recall@5. State it as a sentence: "Hybrid+rerank lifted recall@5 from X% to Y%, a Z-point gain, at the cost of W ms extra latency."

5. **Wire retrieval into the agent loop** - replace the agent's blind `grep`-everything start with a `retrieve()` call that seeds context with the top-k chunks. Re-run a few tasks read-only and eyeball whether the right code now shows up.

**ACCEPTANCE:** A recall@k table across three modes and four k-values, plus a one-sentence lift statement with the latency cost. You can say which mode you'll ship and *why* (it's a recall-vs-latency tradeoff, not a vibe).

**Target number:** recall@5 for `hybrid_rerank`, and the lift over `vector_only`. (This is your retrieval QUALITY number - the roadmap's "vector-only vs hybrid+rerank, with the measured lift.")

---

### Lab 6 - BREAK: context rot by stuffing the window (~1.5h)

**Goal:** Prove that *more* context is not *better* context. Demonstrate, with a number, that performance degrades as you stuff the window.

**Steps:**

1. **Pick 3 tasks** where the agent currently succeeds with `k=5` good chunks.

2. **Stuff the window:** re-run each task feeding `k=30` chunks (the 5 relevant ones buried among 25 irrelevant ones - same total relevant info, far more noise). Keep everything else fixed.

3. **Measure the drop:** does task-completion fall? Does the model cite the wrong file, miss the relevant chunk, or run more steps? Record completion and steps for `k=5` vs `k=30`.

4. **Test compaction as the fix:** add a compaction step - after N tool results, summarize them into a short note and drop the raw results from the window. Re-run the stuffed case *with* compaction. **Does completion recover?**

5. **Document it** in `src/banana/agents/FAILURE_MODES.md`: "Context rot: k=5 → 3/3 pass; k=30 → 1/3 pass; k=30 + compaction → 3/3 pass. More tokens hurt; curation helped."

**ACCEPTANCE:** A before/after showing completion *dropping* when you stuff the window and *recovering* with compaction. You can explain why in terms of attention budget, not hand-waving.

> **Professor's Note - your intuition from databases will mislead you here.** In a database, a bigger index or more cached rows rarely *hurts* a query. In an LLM, more context routinely makes things *worse* - the relevant token gets lost in the noise, and the model's attention is a fixed budget spread thinner. This is counterintuitive for engineers because we're trained that more information is safer. It isn't. The discipline is curation: the fewest, most-relevant tokens that let the model act. "I'll just give it the whole file/repo/history to be safe" is the instinct that quietly tanks your quality. Measure it once, here, and you'll never trust that instinct again.

---

### Deep-Understanding Drill - Week 2

**From-scratch exercise (~40m):** Implement a minimal retriever in **under 40 lines**, no framework, no `banana.agents.retrieval`. Read 5–10 `.py` files, split into function-ish chunks (a regex on `def `/`class ` is fine for the drill), embed with a single Ollama embeddings call per chunk, and cosine-rank against a query. Print the top-3 chunks for one real query. Then, *from memory*, write three sentences: where would BM25 beat this pure-vector version, and why?

**Why:** Retrieval is the part of the agent most likely to be a black box you `pip install`. If you've hand-built cosine ranking over embeddings once, you understand exactly what a vector DB does (and why you don't need one at 200 chunks). And knowing *when lexical beats semantic* - exact identifiers, rare error strings, API names the embedder never saw - is the judgment that makes hybrid search a decision instead of a default.

**ACCEPTANCE:** A standalone script under 40 lines that ranks real chunks for a real query, plus your three-sentence written argument for where BM25 wins.

---

### ✅ Week 2 Checkpoint (pass/fail)

- [ ] tree-sitter chunking produces syntactically-clean function/class chunks with metadata
- [ ] Hybrid retriever (contextual embeddings + contextual BM25 + rerank) behind one `retrieve()` call
- [ ] Retrieval ground-truth set labeled for every golden task
- [ ] recall@k table across 3 modes × 4 k-values, with the hybrid-vs-vector lift stated
- [ ] Context-rot demonstrated (k=5 vs k=30) and compaction shown to recover it
- [ ] Minimal retriever (< 40 lines) works standalone, with a written BM25-wins argument

**Target numbers:** recall@5 (hybrid+rerank) and its lift over vector-only; retrieval p50 latency; completion at k=5 vs k=30.

---

### Socratic Questions - Week 2

1. Your hybrid retriever has recall@5 = 80%. Your agent's task-completion is 40%. **Is the bottleneck retrieval or generation?** What single experiment isolates the answer? (Hint: feed the agent the *known-relevant* chunks directly and re-measure completion.)
2. Contextual Retrieval prepends a blurb to each chunk before embedding. **Why does that help recall - what ambiguity does it remove?** Give a concrete example of two chunks that look identical without their context blurb.
3. You measured context rot: k=30 hurt. **So why not always use k=1?** What's the failure mode of *too little* context, and how do you find the right k without overfitting to these 10 tasks?

---

# WEEK 3 - "Propose, approve, test, report": the supervised loop, end to end, measured

**Theme:** Now the agent earns its name. You add the editing tool, the human approval gate, and full trajectory logging - then close the loop: retrieve → propose diff → *you* approve/reject → run tests → report. And you point the Month 2 harness at the whole thing, producing the month's headline numbers: task-completion %, tool-call accuracy, diff-accept rate.

---

### Concept block (~1.5h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 3.1 (30m) | **Anthropic - "Building Effective Agents"** (re-read the human-in-the-loop + guardrails sections) | Extract: where to put the human checkpoint (before consequential, irreversible actions), and why proposing a diff for approval is strictly safer than applying it. Note the pattern of "agent proposes, human disposes." |
| 3.2 (30m) | **Chip Huyen - *AI Engineering*, agent evaluation section** | Extract the metrics that matter for an agent vs. a single call: task-completion, tool-call accuracy (right tool, valid args), and efficiency (steps). This is what you'll wire into the harness. |
| 3.3 (30m) | **Your own Month 2 eval-standard doc** (`docs/eval-standard.md`) | Re-read what you wrote. The harness scored single outputs. Extract what must change to score an *agent run*: the unit is now a trajectory ending in a diff, and "correct" means the applied diff passes the task's tests. The deterministic oracle is the same `pytest`; the input is now the agent's final diff. |

> **Professor's Note - "supervised" is a feature, not a limitation.** It's tempting to feel like the approval step makes your agent less impressive than the autonomous demos. The opposite is true. The hardest, most valuable agent systems in production in 2026 are human-in-the-loop by design - the agent does the tedious 90% (find the code, draft the change, run the tests) and a human owns the 10% that's consequential (approve the edit). You're not building a weaker agent; you're building the *realistic* one, and you're learning the approval-gate design that every serious agent product needs. Anchor it: this is a deploy pipeline with a manual approval before prod. Nobody calls that "less automated." They call it "not reckless."

---

### Lab 7 - BUILD: the edit tool, the approval gate, and trajectory logging (~3.5h)

**Goal:** The supervised loop, complete. The agent proposes a diff, you approve or reject, approved diffs are applied and tested, and every step is logged as a structured trajectory.

**Steps:**

1. **Add `propose_edit(path, diff)`** to `tools.py` - but it does *not* write to disk. It validates the diff parses and applies cleanly to the current file (dry run), and returns the rendered diff for review. Non-idempotent and consequential → it never auto-applies.

2. **Build the supervisor** (`src/banana/agents/supervisor.py`): when the agent calls `propose_edit`, pause the loop, render the diff to the terminal (red/green), and prompt **[a]pprove / [r]eject / [e]dit-note**. On approve: apply the diff to a working copy and run the task's tests. On reject: feed the rejection (and optional note) back as an observation so the agent can revise. This is the observe→decide→act loop with a human node inserted.

3. **Implement trajectory logging** (`src/banana/agents/trajectory.py`): record the full run as JSONL - every step's thought, tool name, args, `ToolResult`, the proposed diff, your approve/reject decision, and Month 1 telemetry per call. One file per run in `src/banana/agents/trajectories/`. **This is the raw material for Month 4 - design it to be replayable.**

4. **Close the loop** end-to-end on a golden task: agent calls `retrieve()` → reasons → `propose_edit` → you approve → tests run → it reports pass/fail. If tests fail, the agent gets the failure as an observation and may propose a revised diff (bounded by `max_steps`).

5. **Add a `--auto-approve` flag** for *eval runs only* (a human can't sit through 10 tasks × N steps every eval). Auto-approve applies any well-formed diff so the harness can score completion unattended - but the default interactive mode always requires a human. Document why this flag is safe for eval and dangerous in real use.

**ACCEPTANCE:** Interactively, you can drive one golden task from prompt to a passing (or failing) test through approve/reject, watching the diff render and the tests run. The full trajectory is on disk as replayable JSONL. `--auto-approve` lets the run complete unattended.

**Target number:** End-to-end wall-clock for one supervised task (human-in-loop) and one auto-approve task - your two latency points.

---

### Lab 8 - MEASURE: score the agent on the Month 2 harness (~2.5h)

**Goal:** The headline numbers. Run the golden set through the *agent* (auto-approve) and score with your existing harness - task-completion, tool-call accuracy, diff-accept rate - plus steps and cost.

**Steps:**

1. **Adapt the harness entry point** (don't rewrite it): the Month 2 `run_eval` called `client.generate()` on a single prompt. Add a path that instead runs `run_agent(task, ...)` and feeds the agent's *final applied diff* into the same deterministic `test_check`. The oracle is unchanged - only the producer changed.

2. **Define the three agent QUALITY sub-metrics:**
   - **Task-completion %** - applied diff makes the task's `pytest` go green (deterministic, your trustworthy oracle).
   - **Tool-call accuracy** - of all tool calls in a run, what fraction were well-formed and sensible (valid tool, valid args, not a repeat of a just-failed call)? Compute from the trajectory log.
   - **Diff-accept rate** - in *interactive* mode on a sample, what fraction of proposed diffs you accept as-is without an edit-note. (Sample ~10 proposals by hand; this one needs the human.)

3. **Run the full suite** with `qwen2.5-coder:7b`, auto-approve, judge enabled (your calibrated cloud judge from Month 2 scores explanation/quality; deterministic tests own correctness). Save results to `src/banana/evaluation/results/` as usual.

4. **Compare against the Month 2 single-call baseline.** Month 2 scored a single `client.generate()` on the same tasks. Now an *agent* (retrieve + tools + loop) attempts them. **Did the agent beat the single call?** It might not on easy tasks (overhead) and should help on tasks needing multiple files. That contrast is data, not failure.

5. **Run the gate:** `make eval-gate`. The agent must not regress below your established baseline. If it does, you learn that the agent scaffolding *hurt* - an honest, valuable finding.

**ACCEPTANCE:** A results table: task-completion % (by difficulty), tool-call accuracy, diff-accept rate, avg steps, total cost, p50/p95 wall-clock - agent vs. Month 2 single-call baseline. `make eval-gate` runs against the agent.

**Target number:** Agent task-completion % on the golden set (the month's headline QUALITY number) + tool-call accuracy + diff-accept rate.

---

### Lab 9 - BREAK: the agent's real failure modes (~1.5h)

**Goal:** Induce the failures that actually happen in agent runs - not the loop runaways from Week 1, but content failures - and prove your scaffolding handles them.

**Steps:**

1. **Malformed diff:** force the model (small model, high temp) to propose a diff that doesn't apply cleanly. **Does `propose_edit`'s dry-run reject it and feed a useful error back, so the agent revises - instead of corrupting the file?**

2. **Hallucinated file path:** the agent tries to `propose_edit` a file that doesn't exist (it invented the path). **Does the tool return a structured error the agent can recover from?**

3. **Tool timeout mid-run:** make `run_tests` time out on one task. **Does the run survive (timeout → observation → agent reports "tests timed out") rather than hanging or crashing the whole eval?**

4. **Wrong-file edit:** the agent edits a plausible-but-wrong file (tests still fail). **Does your trajectory log let you see it edited the wrong file?** This is the failure category that Month 4's trajectory eval will formalize - note how invisible it is to a pass/fail-only view.

5. **Document all four** in `src/banana/agents/FAILURE_MODES.md` with the trajectory snippet showing the failure and the recovery (or the gap).

**ACCEPTANCE:** All four failures are induced; for each, you can point to either the guard that caught it or the trajectory evidence that exposes it. At least one (wrong-file edit) is something the *number* alone hides but the *trajectory* reveals - write that sentence down for the defense.

> **Professor's Note - the failures that pass-rate can't see.** Task-completion % is a final-answer metric. It tells you the diff worked or didn't. It is blind to *how* - the agent that edited the wrong file three times before stumbling onto the right one scores identically to the one that nailed it in one step. That blindness is exactly why Month 4 exists (trajectory evaluation). You're feeling the gap now, on purpose, so that next month's work has a reason you understand from the inside. The wrong-file edit you just induced is the canonical example: invisible to the score, obvious in the trajectory.

---

### Deep-Understanding Drill - Week 3

**From-memory exercise (~30m):** Draw the complete supervised-agent data/control flow from memory:

```
Task → retrieve(query) → top-k chunks → loop[ observe → DECIDE(client.generate)
  → ACT(tool) → observe ]→ propose_edit(diff) → HUMAN approve/reject
  → apply diff → run_tests → report → trajectory JSONL → Month 2 harness → score
```

For each stage answer: (1) what can go wrong here? (2) which guard or check protects it? (3) is this stage deterministic or model-driven? Then predict: when Month 5 splits this into *multiple* agents (a planner + an editor + a tester), which stages get duplicated, and where's the new failure mode? (Hint: handoffs between agents are where context gets dropped.)

**Why:** If you can draw it and name the failure at each node, you own the system. This diagram is your opening move in the oral defense, and the seed of Month 4's trajectory view and Month 5's multi-agent split.

**ACCEPTANCE:** A flow diagram with a failure-mode and a guard annotated at every stage, saved for the defense.

---

### ✅ Week 3 Checkpoint (pass/fail)

- [ ] `propose_edit` dry-runs and never auto-writes; approval gate works interactively (approve/reject/note)
- [ ] Supervised loop closes end-to-end: retrieve → propose → approve → test → report
- [ ] Full trajectory logged as replayable JSONL (thought, tool, args, result, decision, telemetry)
- [ ] Agent scored on the Month 2 harness: completion %, tool-call accuracy, diff-accept rate
- [ ] Agent compared head-to-head with the Month 2 single-call baseline
- [ ] `make eval-gate` runs against the agent; four content-failure modes induced and documented

**Target numbers:** Task-completion % by difficulty; tool-call accuracy; diff-accept rate; agent vs. single-call delta.

---

### Socratic Questions - Week 3

1. Your agent completes 50% of tasks; the Month 2 single `client.generate()` completed 45%. **Was the agent scaffolding worth it?** Where did it help, where did it just add steps and cost, and how would you decide per-task?
2. Tool-call accuracy is 70% but task-completion is 50%. **What does the 20-point gap tell you?** Can an agent make valid tool calls and still fail the task - what does that look like in a trajectory?
3. You added `--auto-approve` so eval can run unattended. **What exactly does that flag let through that a human would catch?** What's the honest caveat on every auto-approve completion number?

---

# WEEK 4 - "Agent or script? And where does it lose?": the judgment call and the honest gap

**Theme:** The most senior skill in agent engineering isn't building agents - it's knowing when *not* to. This week you stress-test that judgment (run a task a 10-line script does better, and a task that needs an agent), document the honest local-vs-cloud gap, write the 1-pager, and record the defense. Consolidation week.

---

### Concept block (~1.5h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 4.1 (30m) | **Anthropic - "Building Effective Agents"** (final re-read, the "when to use agents" section) | Extract the decision rule in one sentence you can defend: use an agent when the steps can't be known in advance and the task tolerates some error and latency; use a workflow/script when the steps are fixed. Collect the two coding examples you'll put in the 1-pager. |
| 4.2 (30m) | **Chip Huyen - *AI Engineering*, cost/latency of agents** | Extract: an agent multiplies cost and latency by its step count. A 6-step agent is ~6× the calls of a single completion. This is why "agent for everything" is expensive, and why the local-vs-cloud gap matters more for agents than single calls. |
| 4.3 (30m) | **Lilian Weng - "LLM-Powered Autonomous Agents"** (the limitations section) | Extract the documented failure modes - long-horizon planning, error compounding over steps, reliability of tool use. These are the honest limits you'll name in your defense; local 7B will hit them harder than frontier models. |

> **Professor's Note - the senior judgment is subtraction.** Juniors add: another tool, another agent, another step. Seniors ask "can I delete the agent entirely?" The renaming-a-variable-across-files task does not need an agent - it needs `grep -rl` and `sed`, and an agent doing it is slower, costlier, and *less reliable* than the script. The multi-file refactor under a vague spec genuinely needs the agent. Knowing which is which, and being able to say it in a sentence to a skeptical senior engineer, is worth more than any framework you can name. The 1-pager you write this week is the artifact that proves you have this judgment. Most engineers never write it down - they just reach for the agent because agents are exciting.

---

### Lab 10 - BREAK + DEFEND: agent vs. script, head to head (~2h)

**Goal:** Prove the agent-vs-workflow rule with numbers, by finding a task where the agent *loses* to a trivial script and a task where it clearly wins.

**Steps:**

1. **Pick a mechanical task:** "rename `get_user` to `fetch_user` across the repo." Solve it two ways - (a) your agent, (b) a 10-line script (`grep -rl` + `sed`, or `ast` rewrite). Measure both on correctness, latency, and cost.

2. **Pick an open-ended task:** one of your hard golden tasks (a multi-function refactor under a vague spec). Try the script approach - it's not even expressible. Run the agent. This is where the agent earns its existence.

3. **Tabulate the contrast:**

   | Task | Approach | Correct? | Latency | Cost | Verdict |
      |---|---|---|---|---|---|
   | rename across files | script | ? | ? | ~$0 | ? |
   | rename across files | agent | ? | ? | ? | ? |
   | vague multi-file refactor | script | not expressible | - | - | - |
   | vague multi-file refactor | agent | ? | ? | ? | ? |

4. **Write the rule from your own data:** one paragraph - "Use a script when the transformation is mechanical and specifiable; use the agent when the steps depend on reading and reasoning about code you can't enumerate in advance. Here's the proof: the agent was N× slower and M× costlier on the rename, and the only viable option on the refactor."

**ACCEPTANCE:** The contrast table is filled with real numbers, and you have a defensible one-paragraph rule grounded in *your* measurements - the core of the 1-pager.

---

### Lab 11 - MEASURE + DEFEND: the honest local-vs-cloud gap (~2h)

**Goal:** The calibrated-honesty moment. Run the same golden suite through the agent backed by a frontier API and quantify exactly where - and by how much - local loses.

**Steps:**

1. **Swap the agent's backend to a cloud model** (via your Month 1 client's cloud backend - same loop, same tools, same retriever). Run the full golden suite, auto-approve, through the harness.

2. **Produce the gap table:**

   | Backend | Completion % (easy/med/hard) | Tool-call acc | Avg steps | p50 latency | Cost/run |
      |---|---|---|---|---|---|
   | local qwen2.5-coder:7b | ? / ? / ? | ? | ? | ? | ~$0 (electricity) |
   | cloud frontier | ? / ? / ? | ? | ? | ? | $? |

3. **Find the cliff:** at which difficulty tier does local fall off? Usually local holds on easy/medium and collapses on hard (long-horizon planning, error compounding). Name the *specific* failure - "local hallucinated nonexistent APIs on 3/4 hard tasks; cloud did not."

4. **Write the honest gap paragraph:** "Local handles easy/medium at X% - good enough to ship supervised. On hard multi-file tasks it drops to Y% vs. cloud's Z%, failing by [specific mode]. The honest recommendation: run local for the common case, route hard tasks to cloud. The break-even is roughly [cost/quality tradeoff]." (This routing instinct is exactly what Month 10 will formalize.)

5. **Commit the gap table to the repo README.** The number that says "here's where local loses" is the most credible thing in your portfolio.

**ACCEPTANCE:** A local-vs-cloud gap table by difficulty, with the specific failure mode named and a one-paragraph honest recommendation. It's in the README.

**Target number:** The completion-% gap (local vs cloud) on hard tasks - your COST/honest-gap headline.

---

### Deep-Understanding Drill - Week 4

**Explain-it exercise (~30m):** Record a 2-minute voice memo (practice, not the defense) answering a skeptical senior engineer who says: *"Why did you build an agent? Claude Code already exists, and half your tasks could be a shell script."*

Cover: (1) the agent is your learning vehicle and the system-under-test for the eval platform - not a Claude Code competitor; (2) the one-sentence agent-vs-script rule, with your rename-vs-refactor numbers; (3) where your local agent loses to cloud, by the number; (4) one thing you now understand about agents that you couldn't have learned by using one.

**Why:** You will have this exact conversation in interviews and design reviews. The engineer who can say "I built it to understand it, here's the rule for when it's the wrong tool, and here's exactly where mine loses" is more credible than the one demoing an impressive agent they can't critique. Honest limits beat hype.

**ACCEPTANCE:** Recorded, under 2.5 minutes, with at least two real numbers (the agent-vs-script cost gap and the local-vs-cloud completion gap).

---

### ✅ Week 4 Checkpoint (pass/fail)

- [ ] Agent-vs-script contrast table with real numbers; defensible one-paragraph rule
- [ ] Local-vs-cloud gap table by difficulty, with the specific failure mode named
- [ ] Honest-gap recommendation committed to the README
- [ ] 1-pager *"Workflow vs agent"* drafted with a coding example of each
- [ ] Oral defense recorded
- [ ] Repo tagged and public

**Target numbers:** Agent-vs-script cost/latency ratio; local-vs-cloud completion gap on hard tasks.

---

### Socratic Questions - Week 4

1. Your agent is 6× the cost and 8× the latency of a single completion on easy tasks, for the same result. **So why keep the agent at all?** What's the smallest set of tasks where it's actually justified, and how would you route the rest?
2. Local completion on hard tasks is 25%; cloud is 70%. **At what point is "route hard tasks to cloud" the right call vs. "wait for a better local model"?** What would change your answer in six months?
3. You built the control loop by hand this month. **If you adopted LangGraph tomorrow, what exactly would you hand over, and what would you refuse to let it hide?** Where would the framework's defaults hurt you?

---

# End-of-Month Deliverables

---

## Flagship Deliverable: the `banana` Supervised Coding Agent

An increment of `banana` (building directly on the Month 1 client and Month 2 eval harness) that adds:

- **The control loop** (`src/banana/agents/loop.py`): bounded observe→decide→act loop over the Month 1 client, with hard step/token/wall-clock limits and parse-error recovery.
- **Typed tools** (`src/banana/agents/tools.py`): `read_file`, `grep`, `list_dir`, `run_tests`, `propose_edit` - each returning a structured `ToolResult`, validated, with the consequential one gated behind approval.
- **Code-aware retrieval** (`src/banana/agents/retrieval.py`): tree-sitter chunking + contextual embeddings + contextual BM25 + reranking, behind one `retrieve()` call.
- **The supervisor** (`src/banana/agents/supervisor.py`): human approve/reject/edit-note gate that renders diffs and runs tests on approval; `--auto-approve` for eval only.
- **Trajectory logging** (`src/banana/agents/trajectory.py`): replayable JSONL of every step - thought, tool, args, result, decision, telemetry. (The Month 4 substrate.)
- **Harness integration**: the Month 2 `run_eval` now scores agent runs (completion %, tool-call accuracy, diff-accept) against the same deterministic oracle and calibrated judge; `make eval-gate` guards the agent.

### The Three Numbers

| Metric | What it measures | Your number |
|---|---|---|
| **QUALITY** | Task-completion % on the golden set (by difficulty) + tool-call accuracy + diff-accept rate + retrieval recall@5 | _Fill from your harness + recall runs_ |
| **COST** | Local-only vs. cloud-frontier doing the same suite - the honest gap, especially on hard tasks | _Fill from your local-vs-cloud table_ |
| **LATENCY** | Wall-clock p50/p95 per task + steps-to-completion (and retrieval p50 within it) | _Fill from your agent runs_ |

### The Repo

- All agent code wired into `banana` under `src/banana/agents/` (not a separate project)
- Retrieval ground-truth set committed (`src/banana/evaluation/golden/retrieval_truth.jsonl`)
- `src/banana/agents/FAILURE_MODES.md` documenting every BREAK (loop runaway, context rot, malformed/hallucinated diff, tool timeout, wrong-file edit)
- Local-vs-cloud gap table and recall@k table in the README
- `Makefile` targets: `agent` (run interactively), `agent-eval` (score on harness), plus all Month 1–2 targets (`call`, `eval`, `eval-gate`, `viewer`)
- Tagged `v0.8.0` (building on Month 2's `v0.5.0`)
- **Public on GitHub** - the supervised agent is the third major `banana` increment

---

## Portfolio Artifact: the "Workflow vs Agent" 1-pager

A one-page decision doc: `docs/workflow-vs-agent.md`

Structure:
1. **The rule, in one sentence:** use a workflow/script when the steps are knowable in advance; use an agent when they depend on reasoning about input you can't enumerate.
2. **A coding example of each:** the cross-file rename (script - with your measured cost/latency proving the agent loses here) and the vague multi-file refactor (agent - the only viable option).
3. **The cost of getting it wrong:** "agent for everything" multiplies cost and latency by step count for no quality gain on mechanical tasks.
4. **Where the agent itself loses:** the local-vs-cloud gap on hard tasks, by the number, with the routing recommendation.
5. **One honest limitation:** what your supervised agent still can't do (long-horizon planning, error compounding over many steps - the Month 4/5 preview).

Keep it to one page. Real numbers from your own runs. Publish it (blog or repo) - this is the build-in-public artifact for the month.

---

## Oral Defense (~10 minutes, recorded)

Record a screen+voice walkthrough. You must demonstrate LIVE:

1. **Whiteboard the control loop from memory** (~2 min): draw observe→decide→act→repeat, the tools, the three hard limits, and the approval gate. Explain why an agent is "a `while` loop around a model call with tools and a context budget."
2. **Live demo: the supervised loop** (~3 min): run `make agent` on a golden task. Show retrieval pulling chunks, the agent proposing a diff, you approving, tests running, the report. Then reject one proposal and show the agent revise.
3. **Show the numbers and defend them** (~2 min): pull up the harness results - task-completion % by difficulty, tool-call accuracy, diff-accept rate - and your recall@k table. Explain how you measured retrieval *separately* and why that mattered.
4. **Show where it loses** (~2 min): the local-vs-cloud gap table. Name the specific failure mode on hard tasks. State the honest routing recommendation.
5. **Answer aloud** (~1 min): "When is an agent the wrong tool, and how do you know your agent failures are retrieval failures or model failures?" (The honest answer: measure retrieval with recall@k first; and most failures are context, not model.)

---

## Month 3 Final Checkpoint

- [ ] Supervised coding agent works end-to-end: retrieve → propose diff → approve/reject → run tests → report
- [ ] Control loop built from scratch (hand-rolled, < 60 lines core) with hard step/token/time limits
- [ ] Five typed tools with structured `ToolResult`; abuse suite green; `propose_edit` gated behind approval
- [ ] Code-aware retrieval (tree-sitter + hybrid + rerank); recall@k measured across 3 modes; hybrid-vs-vector lift quantified
- [ ] Retrieval measured *independently* of generation
- [ ] Full trajectory logging as replayable JSONL
- [ ] Agent scored on the Month 2 golden set: completion %, tool-call accuracy, diff-accept rate
- [ ] `make eval-gate` runs against the agent; agent compared to the Month 2 single-call baseline
- [ ] Context rot demonstrated and compaction shown to recover it
- [ ] Local-vs-cloud honest gap documented by difficulty, with routing recommendation
- [ ] "Workflow vs agent" 1-pager published
- [ ] Oral defense recorded; repo tagged `v0.8.0` and public

---

# Common Mistakes for Month 3 - Expanded

---

### 1. "Agent for everything"

**What tempts you:** Agents feel powerful and cool. You just built one. So you reach for it on every task - including a cross-file rename a 5-line script does instantly, correctly, and for free.

**What to do instead:** Before building an agent workflow, ask out loud: *"Would a deterministic script do this?"* Renaming a variable across files = script (`grep` + `sed`). Multi-file refactor under a vague spec = agent. You proved this with numbers in Lab 10 - the agent was slower, costlier, *and less reliable* on the mechanical task. Keep that table where you can see it.

**The test:** For the last agent task you ran, could you have written a script that does it more reliably? If yes, you used the agent because it's exciting, not because it's right.

---

### 2. Unbounded loops

**What tempts you:** You forget to set a maximum step count "just for now," the agent gets stuck on a typo, and it runs for hours - burning battery, tokens, and patience while you're at lunch.

**What to do instead:** Hard limits, always, from the first version: max steps, max tokens (summed via Month 1 telemetry), timeout per step *and* per run. You built and BROKE these in Week 1 precisely so they're reflexive. An unbounded local loop doesn't cost API dollars, but it costs hours and a hot laptop - and in production it costs real money.

**The test:** Kill your network mid-run and start a task with no answer. Does the agent stop cleanly at a limit, or does it spin? If you're not *certain* it stops, your limits aren't real.

---

### 3. Blaming the model when retrieval is broken

**What tempts you:** The agent fails a task, the output looks dumb, and you conclude "the 7B model isn't smart enough" - then waste a week on prompt engineering and bigger models.

**What to do instead:** Measure retrieval *separately*. If `recall@k` is low, the right files never reached the window - no prompt tweak fixes that. Feed the agent the known-relevant chunks directly and re-measure: if completion jumps, it was retrieval all along. You built the recall@k harness in Week 2 for exactly this triage.

**The test:** Next failure, before touching the prompt, check recall@k for that task. If the relevant file wasn't in the top-k, you were about to fix the wrong layer.

---

### 4. Over-investing in the agent's quality

**What tempts you:** Making the agent smarter is fun and visible. You spend three weeks adding tools, tuning prompts, chasing the leaderboard - instead of moving on to evaluation depth (Month 4).

**What to do instead:** The agent is a *means* - your learning vehicle and the system-under-test for the eval platform that's the real portfolio crown jewel. Keep it functional and honest; don't try to out-engineer Claude Code. Once it works end-to-end and is measured, move on. The roadmap's value is in the measurement layer, not in a marginally smarter agent.

**The test:** Are you adding a feature because the eval showed a failure mode that matters, or because the feature is cool? Only the first is allowed.

---

### 5. Not measuring retrieval independently

**What tempts you:** You only look at the final output - did the task pass? - and never check whether the retriever found the right files. So you can't tell a retrieval miss from a generation miss.

**What to do instead:** Always report recall@k alongside completion. "Did the retriever find the relevant files?" and "did the model produce a good edit?" are two different questions with two different fixes. You labeled the ground-truth set in Week 2 - use it on every run.

**The test:** Can you state, for your last eval run, both the completion % *and* the recall@5? If you only have one of the two, you can't diagnose your own failures.

---

### 6. (ADDITIONAL) Stuffing the context window "to be safe"

**What tempts you:** When a task fails, the instinct from a lifetime of software is "give it more information" - dump the whole file, the whole module, the whole repo into the window. More context, surely, is safer.

**What to do instead:** You measured the opposite in Lab 6 - k=30 *lost* to k=5. Context is an attention budget, not a hard drive. Curate: fewest, most-relevant tokens, with compaction for long runs. When a task fails, the question is "did the *right* chunk make it in?", not "did *enough* make it in?"

**The test:** When you increase context to fix a failure, did completion actually go up - or did you just feel safer? Re-run and check. If more tokens didn't help, you have a relevance problem, not a quantity problem.

---

### 7. (ADDITIONAL) Auto-approving in real use because the demo did

**What tempts you:** `--auto-approve` made eval runs painless, so you leave it on for real work too - the approval prompt is annoying.

**What to do instead:** Auto-approve is for *unattended eval scoring only*, where a wrong diff just costs a failed test in a sandbox. In real use, the approval gate is the entire point of "supervised" - it's the manual-approval step before prod. Default to interactive; make auto-approve loud and opt-in. Document, on every auto-approve number, that no human vetted those diffs.

**The test:** If `propose_edit` applied a subtly-wrong diff to your actual codebase right now, would anything have stopped it? In interactive mode, you would. In auto-approve, nothing does - which is why it never leaves the eval harness.

---

# Weekly Rhythm Table

A realistic Mon–Sun schedule for someone with a full-time job (~10h/week).

| Day | Time | Activity | Type |
|---|---|---|---|
| **Mon** | 45m | Concept block: Anthropic/Weng/Huyen with a specific question in hand | Read |
| **Tue** | 45m | Concept block: finish the week's reading, take notes | Read |
| **Wed** | 2h | Lab (primary): the week's main BUILD lab | Build |
| **Thu** | 2h | Lab (secondary): MEASURE or BREAK lab | Build |
| **Sat** | 2h | Lab (continued) + Deep-Understanding Drill + trajectory/recall review | Build |
| **Sun** | 1h | Week checkpoint, Socratic questions, reflection journal | Write |
| **Sun** | 1h | 1-pager / repo README / blog progress | Write |

**Totals:** ~2h read · ~6h build · ~2h write = **~10h/week**

> **The iron rule:** If a week is short, **cut the reading first. Never cut the build or the measurement.** A week where you read nothing but built the retriever and measured recall@k is a successful week. A week where you read three agent papers but never ran the loop is a wasted week. The only near-mandatory reading this month is Anthropic's "Building Effective Agents" (Week 1) and "Contextual Retrieval" (Week 2) - everything else can wait. The loop, the tools, the retriever, the harness integration, and the honest gap cannot.

---

# Reflection Journal Prompts

Answer these after each week. Write 5–10 sentences, not paragraphs.

### Every week:
1. **What did I build, and does it work?** (Name the specific artifact and what "works" means.)
2. **What surprised me?** (Surprise = a gap closing. "I expected the agent to beat the single call on easy tasks - it didn't.")
3. **Which Socratic question could I not answer cleanly?** (That's next week's real homework.)
4. **One thing I can now explain to a non-engineer that I couldn't before.**
5. **What number moved this week, and do I understand why?** (Completion %, recall@k, steps, cost - if it moved, name the cause, not just the effect.)

### Week-specific additions:
- **Week 1:** Where did your hand-rolled loop differ from what you expected a framework to do? What did building it yourself reveal that a tutorial would have hidden?
- **Week 2:** What was the single biggest source of retrieval misses? Was it chunking, ranking, or the query? How did you know?
- **Week 3:** When you watched a trajectory of a *failed* task, what did you see that the pass/fail number completely hid?
- **Week 4:** After the agent-vs-script and local-vs-cloud tables - has your instinct for "reach for an agent" changed? Where will you *not* use one now?

---

# "What This Month Sets Up"

You now have a working, measured, supervised coding agent - the system-under-test that the rest of the roadmap evaluates, hardens, and extends. Specifically:

- **Month 4 (Trajectory Evaluation & Failure-Mode Taxonomy)** is built on the trajectory logs you started emitting in Week 3. This month you scored the *final diff*; next month you score the *path* - was the plan sensible, were tool calls efficient, did it edit the right file? The wrong-file edit you induced in Lab 9 (invisible to pass-rate, obvious in the trajectory) is exactly the failure Month 4 formalizes into a taxonomy. Your `src/banana/agents/FAILURE_MODES.md` is its first draft.

- **Month 5 (Multi-Agent Systems)** will split this single agent into a planner + workers and benchmark the result against *this month's single-agent baseline on the same task suite*. The numbers you recorded - completion %, tool-call accuracy, steps, cost - are the bar multi-agent must beat to justify its overhead. Without this baseline, "multi-agent is better" would be another unverified opinion.

- **Month 7 (MCP & A2A)** will wrap your typed tools in the Model Context Protocol so any agent can use them. Because you designed tools as a clean typed API with `ToolResult` contracts (not tangled into the loop), that's an adapter, not a rewrite.

- **Month 10 (Cost-Aware Routing)** formalizes the routing instinct you discovered in Lab 11 - local for the common case, cloud for hard tasks - into a measured router that must hold quality as scored by your harness.

If you skipped this month - if you jumped straight to multi-agent systems or production hardening - you'd have no agent to evaluate, no trajectories to score, no single-agent baseline to beat, and no first-hand understanding of *why* agents fail (it's usually the context, not the model). You'd be tuning a framework you don't understand and calling its failures the model's fault. Instead you built the loop by hand, measured retrieval separately from generation, kept the agent honestly supervised, and pointed your own eval harness at it from day one. That's the difference between someone who runs an agent and someone who can engineer one.

*- End of Month 3 lesson plan. An agent is a `while` loop with tools and a context budget - build the loop, guard the loop, and measure the context. Ask "would a script do this?" before you build, and "is it retrieval or the model?" before you blame. The agent is the means; the measurement is the mastery.*
