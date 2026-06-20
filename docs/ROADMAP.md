# The Applied AI Engineer Roadmap - 18-Month Plan (2026–2028)
### A practical, build-first guide to becoming a production-grade Applied AI Engineer

> **Who is this for?**
>
> A mid-to-senior software engineer who is comfortable with Python, APIs, and systems thinking, and who wants to become an Applied AI Engineer - the person who makes AI systems work reliably in production. You don't need to be in a backend role today (frontend engineers, data scientists, and DevOps professionals all make the jump), but you do need that working foundation - so **start with [Month 0](#month-0--the-on-ramp-before-you-start-month-1) to verify it honestly and close any gaps before Month 1.** No PhD required. No ML research background needed - this is an *applied* roadmap, not a research one.
>
> **What you will build.**
>
> One focused project across 18 months: `banana` - starting as a local AI coding assistant you build from scratch, then evolving into a full Agent Evaluation & Reliability Platform. You build the agent first (so you learn how agents work), then you build the system that makes agents trustworthy enough to ship to real users.
>
> **Why this combination works.**
>
> Building an agent teaches you how AI systems think, fail, and recover. Building the evaluation and reliability layer around it teaches you how to make AI systems *trustworthy*, which is the skill the industry pays the most for in 2026 and beyond.
>
> **Time commitment:**
>
> ~10 hours/week of *focused* work is the planning baseline (~2h reading/theory, ~6h building/measuring, ~2h writing and sharing). **Be honest with yourself: 10 is an average, not a promise.** Some months run hotter - Months 2, 3, 6, and 9 in particular can demand 14–16+ hours during the week or two when a hard build or concept lands - and real life (a work crunch, illness, a lab that just won't pass) doesn't respect a syllabus. That's expected and planned for: the **18 work-months of content are delivered on a 22-month calendar**, with four built-in **buffer / rest months** (one after each of the first four phases) that absorb the overruns and keep you - or your whole cohort - on the same track. See [The Cadence](#the-cadence-and-the-22-month-calendar) below.

> **What this roadmap does NOT cover (and where to go instead).**
>
> Calibrated honesty starts with scope. This plan makes you an *applied* AI engineer who ships reliable systems - it deliberately skips three things:
>
> 1. **Classical ML/DL theory** - no linear algebra, backprop, attention math, or training-from-scratch; you operate models, you don't derive them. *Want that grounding?* Andrew Ng's ML/Deep Learning Specializations, fast.ai, or Karpathy's "Zero to Hero" - *after* or alongside this, not before.
> 2. **Interview-loop grind** - no data-structures-&-algorithms drilling or live system-design rehearsal, which still gate many offers regardless of portfolio. *Go to:* LeetCode/NeetCode for DS&A, and *Designing Data-Intensive Applications* + the "System Design Primer" for the design rounds.
> 3. **Deep cloud & Kubernetes operations** - the build is local-first by design, so no K8s, Terraform/IaC, or provider-specific platform engineering. *When you need it:* the relevant cloud's certification path and the Kubernetes docs.
>
> These are real and worth learning - they're just *adjacent* skills, not this roadmap's job. It tells you where each one bites and points you out the door when it does.

---

## Contents

- [The One Rule That Governs Everything](#the-one-rule-that-governs-everything)
- [Why These Skills Matter](#why-these-skills-matter-the-2026-reality)
- [Phase Overview](#phase-overview-18-work-months-on-a-22-month-calendar)
- [Month-to-Month Dependency Graph](#month-to-month-dependency-graph)
- [The Cadence](#the-cadence-and-the-22-month-calendar)
- [Month 0 - The On-Ramp](#month-0--the-on-ramp-before-you-start-month-1)
- [Phase 1 - Foundations](#phase-1---foundations-months-1-3)
  - [Month 1](#month-1---the-instrumented-ai-client)
  - [Month 2](#month-2--evaluation-driven-development--the-error-analysis-viewer)
  - [Month 3](#month-3--your-first-ai-coding-agent--context-engineering)
- [Phase 2 - Agent Engineering](#phase-2--agent-engineering-months-47)
  - [Month 4](#month-4--trajectory-evaluation--failure-mode-taxonomy)
  - [Month 5](#month-5--multi-agent-systems--orchestration)
  - [Month 6](#month-6--agent-reliability-engineering--human-in-the-loop)
  - [Month 7](#month-7--mcp--a2a-making-the-platform-agent-agnostic)
- [Phase 3 - Production & Performance](#phase-3--production--performance-months-811)
  - [Month 8](#month-8--inference-optimization-local)
  - [Month 9](#month-9--safety-security--guardrails)
  - [Month 10](#month-10--cost-aware-model-routing)
  - [Month 11](#month-11--productionize--the-justified-customization-decision)
- [Phase 4 - The Evaluation Platform](#phase-4--the-evaluation-platform-months-1214)
  - [Month 12](#month-12--the-agent-evaluation-platform)
  - [Month 13](#month-13--observability--telemetry-layer)
  - [Month 14](#month-14--advanced-reliability--second-system-under-test)
- [Phase 5 - Leadership & Capstone](#phase-5--leadership--capstone-months-1518)
  - [Month 15](#month-15--the-paved-road-platform-sdk)
  - [Month 16](#month-16--technical-leadership-artifacts)
  - [Month 17](#month-17--portfolio-polish--open-source-contribution)
  - [Month 18](#month-18--capstone-integrate-narrate-prove)
- [Consolidated Reference](#consolidated-reference)

---

## The One Rule That Governs Everything

**Every deliverable earns three numbers: QUALITY, COST, and LATENCY.**

- **QUALITY** = Does it work? How often? How well?
- **COST** = How much does it cost to run? (money, time, compute)
- **LATENCY** = How fast is it? How long does the user wait?

A claim without a number is just an opinion. This rule never changes across all 18 months.

---

## Why These Skills Matter (The 2026 Reality)

The AI industry has shifted. Companies no longer need people who can build demos, they need people who can build AI systems that work reliably in production, every day, at scale.

**What hiring managers look for in 2026:**

| Skill                                                 | Why it matters                                                                                                                                                                                     | Where you learn it |
|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| **Error analysis - looking at the data**              | The #1 highest-return activity in AI development. Teams that do this well iterate 10x faster.                                                                                                      | Months 2, 4, throughout |
| **Evaluation design - deciding what to measure**      | The judgment of constructing the right tests for non-deterministic software.                                                                                                                       | Months 2, 4, 8 |
| **System architecture for non-deterministic systems** | 95% reliability per step = only ~60% reliability over 10 steps. Understanding compounding error changes how you design everything.                                                                 | Months 3, 5, 6 |
| **Reliability engineering for agents**                | Gartner predicts >40% of agentic AI projects will be cancelled by end of 2027, mostly on runaway cost, unclear value, and weak reliability/risk controls. Owning reliability is rare and valuable. | Months 6, 9, 14 |
| **Cost/latency/quality tradeoff judgment**            | Model routing, prompt caching, and context/token reduction are the primary levers for agent cost in 2026.                                                                                          | Months 10, 11 |
| **Context engineering**                               | The 2026 successor to prompt engineering: managing what data goes into the AI's "working memory" at every step.                                                                                    | Months 3, 5 |
| **Technical writing & influence**                     | Senior-level output is decisions expressed through writing. Frontier lab job descriptions literally list "publish and speak."                                                                      | Months 15, 16, throughout |
| **Protocol fluency (MCP / A2A)**                      | MCP is the standard for connecting AI to tools; A2A is the standard for agents talking to agents. Both under the Linux Foundation now.                                                             | Months 7, 12 |
| **Security & safety**                                 | OWASP now has two AI security frameworks (LLM Top 10 and Agentic Top 10). A coding agent with shell access is a real security risk.                                                                | Months 9, 13 |
| **Build-vs-buy judgment**                             | "Should we fine-tune? Use an agent? Buy a vendor solution?" - the calibrated-honesty calls that define seniority.                                                                                  | Months 11, 15 |

---

## Phase Overview (18 Work Months on a 22-Month Calendar)

| Phase | Work months | Theme | What you can do after |
|-------|-------------|-------|-----------------------|
| **1. Foundations** | 1–3 | Build the AI client, learn evaluation, build your first agent | You can build and measure AI-powered tools |
| *↻ Buffer & Rest* | *+1 month* | *Catch up, consolidate, rest - or self-study an adjacent skill* | *You (or the cohort) are re-synced for Phase 2* |
| **2. Agent Engineering** | 4–7 | Multi-agent systems, reliability, protocols, context engineering | You can design and harden production agents |
| *↻ Buffer & Rest* | *+1 month* | *Catch up, consolidate, rest - or self-study an adjacent skill* | *You (or the cohort) are re-synced for Phase 3* |
| **3. Production & Performance** | 8–11 | Optimization, cost routing, customization, security | You can run agents fast, cheap, and safe |
| *↻ Buffer & Rest* | *+1 month* | *Catch up, consolidate, rest - or self-study an adjacent skill* | *You (or the cohort) are re-synced for Phase 4* |
| **4. Evaluation Platform** | 12–14 | Trajectory eval, observability, the platform that makes agents trustworthy | You can evaluate and improve any agent |
| *↻ Buffer & Rest* | *+1 month* | *Catch up, consolidate, rest - or self-study an adjacent skill* | *You (or the cohort) are re-synced for Phase 5* |
| **5. Leadership & Capstone** | 15–18 | Platform SDK, technical writing, capstone, career positioning | You can lead AI engineering for a team |

> *Month numbers (1–18) are **work months** of `banana` content. The four buffer/rest months are extra calendar time **between** phases, which is why 18 work-months span a ~22-month calendar.*

---

## Month-to-Month Dependency Graph

The full dependency graph lives in [`dependencies-graph.md`](./dependencies-graph.md). It is the visual companion to this roadmap: use it to see the critical path, the long-range artifact reuse, and why each month needs the prior month's deliverables to be real before moving on.

---

## The Cadence and the 22-Month Calendar

**This roadmap is a strict chain: every month extends the previous month's `banana` codebase, so you cannot really start month N until month N−1's deliverables are real.** That makes it powerful (everything compounds) and fragile (one stalled month can topple the rest). The four buffer months are the shock absorber that keeps the chain from snapping.

**The rule:** after each of the first four phases, take **one buffer / rest month** - no new `banana` content. (Phase 5 needs no buffer; finishing the capstone *is* the finish line.) These months do two jobs:

1. **Absorb overruns.** The ~10 h/week budget is an average, and Months 2, 3, 6, and 9 routinely spike past it. A buffer means a heavy phase doesn't cascade into you falling behind forever - you finish the phase *properly* instead of half-finishing it and limping into the next one on a broken foundation.
2. **Re-synchronize a cohort.** If you're learning with others, fast finishers wait here while everyone catches up, so the whole group enters the next phase together. Solo learners get the same benefit against their own schedule.

### If you're *behind* when a buffer month starts

Use the whole month to finish the phase. **Do not start the next phase until every `✅` checkpoint in the prior phase passes and your three numbers are real.** That is the entire point of the buffer - protecting the dependency chain is more valuable than staying on the calendar. Finishing "on time" means finishing the phase *well*, not racing the clock.

### If you're *already done* when a buffer month starts (the wait-time menu)

You've earned slack - spend it deliberately. **Rest first** (burnout is the real project-killer over 22 months), then pick from this menu. The buffers are also the natural home for the *adjacent* skills this roadmap deliberately skips (see the "does NOT cover" box above):

| Buffer (after) | Consolidate / review | Or self-study an adjacent skill (where it pays off next) |
|----------------|----------------------|----------------------------------------------------------|
| **Phase 1** (Foundations) | Refactor the rushed parts of your client + eval harness; polish the error-analysis viewer; write the Month 2 blog post properly. | **DS&A warm-up** (LeetCode/NeetCode) - keeps the interview muscle alive early. |
| **Phase 2** (Agent Engineering) | Deepen trajectory eval; tidy the multi-agent state schema; improve your worst number. | **System-design practice** - pairs naturally with the architecture thinking you just used. |
| **Phase 3** (Production & Performance) | Re-run the full eval after your optimizations; document the routing rules; load-test what you've built. | **A little ML/DL theory** - just enough to sharpen your quantization- and fine-tuning-quality intuition from Months 8 & 11. |
| **Phase 4** (Evaluation Platform) | Hunt remaining integration seam bugs; draft the Month 16 RFC early. | **Cloud / K8s / IaC basics** - the deployment skills you'll want before taking the platform public. |

Two more high-leverage options at any buffer:

- **Go deeper on the phase you just finished** - the optional/stretch labs you skipped, a second model backend, a harder benchmark.
- **Help the cohort.** Review someone else's traces, pair on a stuck lab. Teaching is the best consolidation there is - and it's a rehearsal of the Month 16 leadership skill, practiced early.

> **Professor's note.** Buffers are part of the plan, not a confession of failure. The engineers who finish this roadmap are not the fastest ones - they're the ones who protected the chain, rested before they burned out, and arrived at each phase on a foundation that actually held. Plan the 22 months. Respect the four off-ramps.

---

# MONTH 0 - The On-Ramp (Before You Start Month 1)

> **Read this first. It is the one part of the roadmap with nothing to ship - and skipping it is the most common reason people stall around Month 2.** This roadmap assumes you are already a working software engineer. It does **not** teach you to program. Before Month 1, *verify* you have the foundation - don't assume it. A missing prerequisite doesn't disappear; it ambushes you in Month 3 when you're already busy learning how agents fail.

"Mid-to-senior engineer" hides enormous variance in the skills *this* roadmap leans on. A backend engineer who writes async services daily is ready tomorrow. A frontend engineer who's spent years in React, or a data scientist who lives in notebooks, is plenty senior but has real gaps to close first - and that's fine, as long as you close them *now*, on purpose, instead of discovering them mid-Month-3. Month 0 is a half-day diagnostic plus, if needed, 20–40 hours of targeted pre-work. Treat it as the cheapest insurance in the whole plan.

## Step 1 - The Diagnostic (be honest; it takes ~30 minutes)

For each item below, ask: *could I do this right now, in a few minutes, without googling the basic syntax?* "I've seen it" is not "I can do it." **Must-haves** are non-negotiable for Month 1. **Strong-to-haves** you can pick up just-in-time, but gaps will slow you down in the month named.

**Must-haves (needed for Month 1):**

| Skill | The honest test | If you can't |
|-------|-----------------|--------------|
| **Python (intermediate)** | Write a class with a context manager that times the code inside its `with` block. | Pre-work A |
| **Async Python** | Fetch 3 URLs concurrently with `asyncio` and return when all finish. | Pre-work B |
| **HTTP / REST / streaming** | Explain what a `429` means, how you'd back off, and what a streamed (SSE/chunked) response is. | Pre-work C |
| **Typed data & JSON** | Validate a model's JSON output against a schema (pydantic/dataclass) and handle a malformed field without crashing. | Pre-work D |
| **Git** | Branch, commit, diff, and resolve a merge conflict; revert one change to a versioned file. | Pre-work E |
| **CLI / shell** | Set an env var, run a script, capture stderr separately from stdout. | Pre-work E |
| **Testing basics** | Write a `pytest` test that *fails the build* when a number drops below a threshold. | Pre-work F |

That last one isn't hypothetical - it's literally what you build in Month 2 (the CI gate). If it sounds foreign now, that's exactly the gap to close before you start.

**Strong-to-haves (pick up just-in-time, but know the gap):**

| Skill | First bites in | Why |
|-------|----------------|-----|
| Basic SQL | Month 3, 13 | Querying logs/traces and retrieval metadata. |
| A minimal UI (Streamlit / Flask / plain HTML) | Month 2 | The error-analysis viewer. Plain HTML over JSONL is enough. |
| Regex | Month 2, 3 | Deterministic checks and chunking. |
| Docker basics | Month 11, 13 | Packaging and self-hosting Langfuse. A `docker compose up` is the floor. |
| OS / sandboxing literacy (processes, permissions, path allowlists) | Month 9 | Sandboxing a shell-capable agent. |

**Explicitly NOT required** (you learn these just-in-time as disposable scaffolding, or not at all): machine-learning or deep-learning theory, linear algebra, the math of transformers and attention, training dynamics, or any prior AI/ML project. This is an *applied* roadmap. You will operate LLMs without first deriving them - and where that absence bites (reasoning about quantization quality loss in Month 8, debugging a fine-tune in Month 11), the roadmap tells you and gives you the just-in-time intuition you need. Do **not** spend Month 0 on a deep-learning course. That's the Month 1 "transformer math rabbit hole" mistake, arriving early.

## Step 2 - The Pre-Work (close the gaps, time-boxed)

Only do the rows you failed. Time-boxes are honest upper bounds; stop early if it clicks. Resources are named generically on purpose - use whatever current edition you find; don't shop for the "perfect" course (that's procrastination).

| Gap | Pre-work | Time-box | Done when |
|-----|----------|----------|-----------|
| **A - Python** | Python's official tutorial (classes, comprehensions, context managers, decorators) + set up a project with `uv` or `poetry`. | 8–15 h | You can scaffold a typed module with a virtualenv from scratch. |
| **B - Async** | A focused async/await guide; practice `asyncio.gather` and a semaphore-bounded fetch. | 6–10 h | Your concurrent-fetch test passes and you can explain *why* it's faster. |
| **C - HTTP** | MDN's HTTP overview + read your chosen LLM provider's API reference end-to-end, including streaming. | 3–6 h | You can describe a request's full lifecycle and what streaming changes. |
| **D - Typed data** | The pydantic (or dataclasses) docs; build one validator with a custom error path. | 3–5 h | You parse-and-validate a deliberately malformed JSON without an unhandled exception. |
| **E - Git & shell** | "Pro Git" chapters 2–3; practice forcing and resolving a conflict; basic shell redirection. | 2–4 h | You resolve a conflict and revert a single commit without panic. |
| **F - Testing** | The `pytest` getting-started docs; write a fixture and a threshold assertion. | 3–5 h | You have a test that goes red when a metric regresses. |

### The exit gate: a 50-line warm-up build

Reading isn't proof. **Demonstrate** the prerequisites with a tiny build that is a micro-version of Month 1:

> Write a ~50-line script that (1) sends one prompt to a model - a cloud API *or* local Ollama, your choice - (2) parses the response as JSON against a small schema, (3) retries with backoff on a failed call or a parse error, and (4) prints **tokens used, latency, and (for cloud) cost**.

If you can write that comfortably, you are ready for Month 1 - and you've already met **The One Rule** (QUALITY, COST, LATENCY) on day zero. If that script fights you, finish the pre-work first. Month 2 is genuinely hard; you do not want to be learning the language *and* evaluation-driven development at the same time.

> **Professor's note.** Pre-work is scaffolding, not the building. Cap it. If you're 80% comfortable, start Month 1 and patch the last 20% just-in-time - you learn faster against a real task than against a tutorial. The failure mode here is the mirror of the Month 1 rabbit hole: spending six weeks "getting ready" and never starting. Set the time-box, hit it, move.

## Step 3 - Pick Your Hardware Track

You do **not** need a Mac, a GPU, or a powerful machine to follow this roadmap - about 90% of the work (eval, trajectory eval, reliability, MCP, safety, routing, observability, the platform, the SDK, and all the leadership/portfolio work) is plain Python + APIs that runs on anything. Pick the track that matches the hardware you already own. (See the **Hardware Requirements** section near the end for the memory-budget details.)

| Track | You have | How you'll run models |
|-------|----------|-----------------------|
| **A - Full local** | ~16 GB+ unified RAM / VRAM, or 32 GB+ for the recommended tier | Run 7B–32B models locally as written. This is the default the roadmap assumes. |
| **B - Low-end local + cloud** | <16 GB, weak GPU, or CPU-only | Run *small* models locally (slowly) for the mechanics; route real generation to a cloud API. You skip nothing conceptually. |
| **C - No capable hardware** | A light laptop / Chromebook-class machine | Cloud APIs for generation; use **Google Colab or Kaggle free GPU sessions** for the handful of GPU-only labs. |

**The low-end / cloud-substitute itinerary.** Only a few months are hardware-sensitive. Here's the equal path for Tracks B and C:

| Month | What it normally wants | Low-end / cloud substitute |
|-------|------------------------|----------------------------|
| **M1** | Ollama **+** a second *local* backend (MLX/llama.cpp) | Ollama with one small model **+** a second *cloud* provider behind the same interface. **Honesty caveat:** you'll measure local-vs-cloud, not local-vs-local - note that in your write-up. |
| **M8** | Speculative decoding + quantization tuned to local hardware | Speculative decoding is effectively GPU/Apple-only. On CPU, do the **quantization-frontier + caching** labs (they transfer), and rent a cloud GPU *once* (or use Colab) to *observe* speculative decoding - this is the same one-off cloud comparison the month already prescribes. Expect small local numbers; the *technique and the reasoning* are what transfer. |
| **M11** | Optional on-device LoRA (mlx-lm / Unsloth) | Use a **managed cloud LoRA** or a Colab/Kaggle GPU session. On-device fine-tuning is the fast lane, never a requirement. |
| **M13** | Self-hosted Langfuse | `docker compose up` locally (cheap on CPU) or a small free-tier cloud instance. |

Budget a modest amount of cloud credit for Tracks B and C. The measurement and caching/routing discipline you build from Month 1 onward is exactly what keeps that spend small - you'll know what every call costs and you'll cache and route to avoid the expensive ones.

> **Windows note.** Use **WSL2**. Several local runtimes and the container tooling assume a Unix-like environment; WSL2 gives you that without dual-booting.

### ✅ Month 0 Checkpoint (pass/fail)

- [ ] You passed the diagnostic, or closed **every must-have** gap with pre-work.
- [ ] The 50-line warm-up build runs: it calls a model, parses JSON, retries on failure, and prints **tokens + latency** (and cost, if cloud).
- [ ] You've picked your hardware track and confirmed you can run - or cloud-substitute - a model end-to-end.

Three checks pass → start Month 1. Any check fails → finish the pre-work first. There is no shame in spending three weeks here; there is real pain in skipping it.

---

# PHASE 1 - FOUNDATIONS (Months 1-3)

*Goal: Build the reliable base components that everything else depends on.*

---

## Month 1 - The Instrumented AI Client

**What you are building:**

A reusable module that talks to AI models, both cloud APIs (like OpenAI, Anthropic, Google) and local models (via Ollama plus a second local backend: MLX on Apple Silicon, or llama.cpp on an NVIDIA GPU / CPU). One clean interface that works with any provider.

**What you will learn:**
- How AI models actually work at the API level: tokens, context windows, temperature, top_p, and how they change the output
- How to measure everything: tokens per second, time to first response, cost per call, memory usage
- How to build a clean SDK with retry logic, error handling, and structured output parsing
- The difference between local inference (free but slower) and cloud APIs (fast but costs money)

**What "done" looks like:**
- A Python module that sends the same prompt to 3 different backends (cloud API, local Ollama, and a second local backend - MLX on Apple Silicon or llama.cpp on GPU/CPU) behind one interface
    - **No capable local hardware?** The floor is cloud API **+** Ollama (one small model) **+** a *second cloud provider* behind the same interface. You'll then measure local-vs-cloud rather than local-vs-local - call that out honestly in your write-up. (See the low-end / cloud-substitute itinerary in Month 0.) The interface is the deliverable; the second backend being *local* is the fast lane, not the requirement.
- Every call automatically logs: tokens used, cost, latency (time-to-first-token and total), and memory usage
- A small experiment showing how changing temperature and top_p affects output quality and parse-failure rate, with actual numbers

**Your three numbers:**
- **LATENCY:** Time-to-first-token and tokens/sec for at least 2 model sizes locally vs cloud
- **QUALITY:** Parse-failure rate across different sampling settings
- **COST:** Local cost (electricity + time) vs cloud API cost per call

**Portfolio artifact:**

A 1-page write-up: *"Local vs Cloud AI - when to use which, with numbers from my machine."*

**Reading list:**
- Chip Huyen - *AI Engineering* (start now, return all year)
- Ollama docs + your second backend's README (MLX/`mlx-lm` on Apple, or llama.cpp on GPU/CPU)
- Anthropic or OpenAI API docs
- Andrej Karpathy - "Intro to LLMs" video (for intuition only)

### Common Mistakes in Month 1 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Falling into the transformer math rabbit hole** | You start reading about attention heads and matrix multiplication and spend weeks on theory | Cap at intuition. You need to *use* models, not redesign them. Watch Karpathy's video once and move on. |
| **Rebuilding LangChain from scratch** | You think you need a full framework before you can do anything | Build only the thin layer you understand. A clean API wrapper with retry logic is enough. |
| **Blindly adopting a framework** | You install LangChain/LlamaIndex on day 1 and let it do everything | Build your own simple client first. You need to understand what happens on every API call. Add frameworks later when you know *why* you need them. |
| **Not measuring from day one** | "I'll add telemetry later" | No. Bake cost/latency/quality tracking into every call from the start. This is the foundation everything else depends on. |
| **Trying to run models that are too large** | You download a 70B model on a 16GB machine and wonder why it's slow (or the GPU just runs out of memory) | Start with models that fit comfortably: 7B-14B on 16GB, up to 32B on 32GB+ (unified RAM on Apple, VRAM on a GPU, system RAM on CPU). Match the model to your hardware. |

</details>

---

## Month 2 - Evaluation-Driven Development & The Error-Analysis Viewer

**What you are building:**

A test harness for AI systems - the equivalent of a test suite for non-deterministic software. Plus a simple viewer that lets you look at failures and understand *why* things went wrong.

**Why this comes so early:**

Evaluation is the #1 most valuable skill in AI development. Teams that build custom tools to look at their data iterate 10x faster than teams that rely on vibes. If you only master one thing from this entire roadmap, master this.

**Go deep on two; be aware of the rest.**

This is a spike month - six topics below, but only two are mastery targets: (1) **building the error-analysis viewer and actually using it** to hand-label ~50 failures (this is skill #1 in the whole roadmap), and (2) **calibrating the LLM judge** against your own labels (Cohen's κ + the position / verbosity / self-enhancement biases). Everything else is *awareness*: treat the L1/L2/L3 hierarchy as shared vocabulary, know that L3 (A/B in production) exists without building it, and read promptfoo / DeepEval for patterns rather than adopting either wholesale. If the month runs past your hours, protect the two; let the rest stay shallow.

**What you will learn:**
- The three-level eval hierarchy practitioners actually use (Husain): **L1** assertion/unit-test checks distilled from real production samples, **L2** human + LLM-as-judge review, **L3** A/B testing in production
- How to test AI outputs: deterministic checks (does the code compile? do tests pass?) vs AI-as-judge (is the output high quality?) vs human evaluation
- How to build golden datasets - curated examples with known-good answers that you grow from real failures
- How to calibrate an AI judge: measuring how often it agrees with human labels (report **Cohen's κ** for categorical labels, not just raw agreement %), and the known biases to control for - **position bias**, **verbosity bias** (judges prefer longer answers >90% of the time), **self-enhancement bias** (models favor their own outputs)
- **Criteria drift**: your own pass/fail criteria will evolve as you look at more outputs - expect it, and re-version your rubric when it happens
- How to build an error-analysis viewer: a simple UI where you can scroll through traces, label failures, and discover patterns. Prefer **binary pass/fail over Likert scales**, and remove *all* friction from looking at data

**What "done" looks like:**
- An eval harness with deterministic checks + AI-as-judge scoring + judge calibration script
- A versioned set of coding tasks (bugs to fix, features to add) with known-good solutions, aligned to the SWE-bench format so your numbers are meaningful to anyone
- A simple error-analysis data viewer (even a terminal UI or basic web page) where you can browse results and label failures
- A CI gate that fails a pull request if quality drops below your baseline
- Judge calibration results showing agreement with ~30 of your own human labels - run for both a large and a small model and show the gap

**Your three numbers:**
- **QUALITY:** Pass rate on the coding task suite + judge score
- **Judge calibration:** % agreement with human labels (big model vs small model)
- **COST/LATENCY:** Time and memory to run the full eval (must be cheap enough to run on every PR)

**Portfolio artifact:**

An "evaluation standard" document + a blog post *"Why your AI eval is lying to you (and the data viewer that fixes it)."*

**Reading list:**
- Huyen - *AI Engineering* (eval chapters)
- **Hamel Husain - "A Field Guide to Rapidly Improving AI Products"** (mandatory - this single essay will reshape how you think about AI development) + his earlier "Your AI Product Needs Evals" (the three-level hierarchy)
- **Eugene Yan - "Evaluating the Effectiveness of LLM-Evaluators (LLM-as-Judge)"** (the biases and how to measure judge–human agreement)
- **"What We Learned from a Year of Building with LLMs"** (applied-llms.org) - the field's most-cited production lessons essay
- SWE-bench / **SWE-bench Verified** methodology (Verified is the trusted human-validated subset cited in model releases)
- promptfoo or DeepEval docs (for patterns, not to adopt wholesale)

### Common Mistakes in Month 2 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Vibes-based development** | "It feels better" is easier than measuring | Define pass/fail criteria *before* running evals. Never merge without checking the numbers. |
| **Trusting a small local AI judge blindly** | Small models hallucinate agreement and favor longer answers even more than big models | Always calibrate: compare judge scores against your own human labels. Report the agreement rate. Use deterministic checks (compile, test, diff) wherever possible - for code, that's most places. |
| **Building the harness but skipping the "what to measure" work** | The plumbing (running tests, computing scores) feels more engineering-like | The plumbing is commoditized. The *judgment* of what failure modes matter and how to detect them is the prize. Spend time in your data viewer looking at failures. |
| **Single-number theater** | Reporting one accuracy number without error bars or context | Always report confidence intervals on small sample sizes. "87% ± 12%" is honest; "87%" alone is misleading when n=30. |
| **Not versioning your golden dataset** | You keep editing the test cases and lose track of what changed | Version it in git. Track every addition and removal. Never test on examples the model was trained on. |

</details>

---

## Month 3 - Your First AI Coding Agent + Context Engineering

**What you are building:**

A supervised coding agent - an AI that retrieves relevant code, proposes edits as diffs, waits for your approval, runs tests, and reports the results. Think of it as a junior developer in your terminal that always asks before making changes.

**Why "supervised"?** At this stage, local models are not reliable enough to act alone. And honestly, even frontier models should have human oversight for consequential actions. The supervised model is both realistic and teaches you human-in-the-loop design.

**What you will learn:**
- The agent control loop: observe → decide → act → repeat
- Tool design as API design: typed, idempotent tools like `read_file`, `grep`, `propose_edit`, `run_tests`
- **Structured-output & tool-call reliability**: getting the model to emit tool calls that actually *parse and validate* every time. The ladder from cheapest to strongest - structured-output/JSON mode → grammar-constrained decoding (Outlines, llama.cpp GBNF) → reprompt-and-repair loop → strict schema validation (pydantic). This is the daily failure mode of real agents, it compounds exactly like the Month 4 reliability math, and it's where small/local models lose hardest to frontier
- Context engineering: how to get the *right code* into the AI's context window (code chunking with tree-sitter, hybrid retrieval with BM25 + vector search, reranking). Anthropic's **Contextual Retrieval** recipe - contextual embeddings + contextual BM25 + reranking - cut retrieval failure ~67% in their tests; treat that stacked recipe as your default, not naive vector search
- **Context rot**: model performance degrades as the window fills (you have a finite "attention budget"), so curating *fewer, better* tokens beats stuffing the window. Learn compaction and external note-taking as first-class techniques
- When to use an agent vs when a simple script is better (the single most important judgment call in agent engineering)
- **Lightweight structured tracing**: record every run as spans (thought → tool-call → result → approval) in a simple local format from day one. This is your observability foundation - any past run must be replayable from it. You *productionize* these spans into OpenTelemetry + Langfuse with drift detection, governance, and dashboards in Month 13; for now keep it minimal but complete. (These traces capture source code and can capture secrets/PII, so treat them as sensitive from the first run - you harden redaction/retention in Months 9 and 13.)

**What "done" looks like:**
- A working supervised coding agent: retrieve context → propose diff → you approve/reject → run tests → report
- Every step logged as a complete trajectory (thought, tool call, result, approval decision) - and **any past run is replayable step-by-step from its trace alone**. This local span format is the seed of the Month 13 observability layer; Month 13 productionizes it (OpenTelemetry → Langfuse, drift, dashboards), it does not replace it
- Evaluated on your Month 2 golden set: task completion %, tool-call accuracy, % of diffs accepted as-is
- **Tool-call reliability measured**: % of tool calls that *parse and validate* against schema, plus the malformed-/wrong-tool rate - reported for a local model vs a frontier model (the honest gap), with the repair-ladder lift shown
- Retrieval quality measured independently: recall@k for "which files are relevant to this change"
- A comparison: vector-only retrieval vs hybrid+rerank, with the measured lift

**Your three numbers:**
- **QUALITY:** Task completion + tool-call reliability (parse+validate rate, malformed-call %) + diff-accept rate
- **COST:** Local-only vs cloud API doing the same tasks (the honest gap)
- **LATENCY:** Wall-clock time + steps-to-completion

**Portfolio artifact:**

The agent repo + a 1-pager *"Workflow vs agent: the rule, with a coding example of each."*

**Reading list:**
- Anthropic - "Building Effective Agents" (the workflow-vs-agent distinction and the six core patterns)
- Anthropic - "Effective Context Engineering for AI Agents" (context rot, compaction, note-taking)
- LangChain (Harrison Chase) - "The Rise of Context Engineering"
- Chip Huyen - "Agents"
- Lilian Weng - "LLM-Powered Autonomous Agents"
- Anthropic - "Contextual Retrieval"
- tree-sitter docs (for code-aware chunking)

### Common Mistakes in Month 3 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **"Agent for everything"** | Agents feel powerful and cool, so you use them for tasks a 5-line script could handle | Before building an agent workflow, always ask: "Would a deterministic script do this?" Renaming a variable across files = script. Multi-file refactor under a vague spec = agent. |
| **Unbounded loops** | You forget to set a maximum number of steps, and the agent runs for hours | Set hard limits: max steps per task, max tokens per run, timeout per step. An unbounded local loop still burns hours of battery and patience. |
| **Blaming the model when retrieval is broken** | "The model is dumb" is often actually "the wrong files were in context" | Measure retrieval quality separately from generation quality. If recall@k is low, fix retrieval first. Most prompt-tuning is wasted effort when the context is wrong. |
| **Treating a malformed tool call as a model-quality problem** | A call that won't parse or validate looks like "the model is bad" | Separate *machinery* failures (unparseable/invalid tool calls) from *judgment* failures (a valid call, wrong choice). Fix the machinery first with constrained decoding + a repair loop - don't burn the prompt budget on a parsing bug. |
| **Over-investing in the agent's quality** | You spend weeks making the agent smarter instead of moving to evaluation | The agent is a means to an end - your learning vehicle and future system-under-test. Keep it functional but don't obsess over making it compete with Claude Code. |
| **Not measuring retrieval independently** | You only check the final output and never know if the right files were found | Always report recall@k: "did the retriever find the relevant files?" separately from "did the model produce a good edit?" |

</details>

---

# PHASE 2 - AGENT ENGINEERING (Months 4–7)

*Goal: Go from a single agent to multi-agent systems, make them reliable, and learn the protocols that make them interoperable.*

---

## Month 4 - Trajectory Evaluation & Failure-Mode Taxonomy

**What you are building:**

The "hard kind" of agent evaluation - scoring not just whether the agent got the right answer, but whether it took a sensible *path* to get there. Plus a living catalog of failure modes.

**Why this matters:**

Most people only check the final output. But an agent that gets the right answer by reading 50 irrelevant files and making 12 unnecessary tool calls is fragile - it just got lucky. Trajectory evaluation catches these problems before they become production incidents.

**What you will learn:**
- Step-level evaluation: was the right file read? Was the plan sensible? Were tool calls efficient?
- Compounding error math: if each step is 95% reliable, 10 steps = only 60% reliability. This changes how you design everything.
- **Reliability vs. capability**: borrow the **pass^k** metric from Sierra's **τ-bench** - run the *same* task k times and measure how often it succeeds *every* time. Agents that score ~50% on pass^1 often collapse to ~25% on pass^8. Your agent isn't done when it passes once; it's done when it passes consistently.
- Failure-mode taxonomy: categorizing *why* the agent fails (wrong files retrieved, bad plan, tool call error, etc.) and how often each failure type occurs
- How to turn raw failure traces into a prioritized "what to fix next" list

**What "done" looks like:**
- A trajectory eval suite that scores the *path*, not just the final output
- A documented failure-mode taxonomy with frequencies (e.g., "wrong file retrieved: 35% of failures; bad plan: 20%")
- Trajectory pass-rate shown to be different from output pass-rate (they will diverge - that's the insight)
- At least one fix driven by the taxonomy that demonstrably moves a number

**Your three numbers:**
- **QUALITY:** Trajectory pass-rate (distinct from output pass-rate)
- **TAXONOMY:** Number of failure categories with frequencies
- **IMPROVEMENT:** At least one metric improved by fixing a specific failure mode

**Portfolio artifact:**

A blog post *"Scoring the path, not the answer: trajectory eval for agents."*

**Reading list:**
- Sierra - "τ-bench: A Benchmark for Tool-Agent-User Interaction" (the pass^k reliability metric)
- SWE-bench Verified (how the trusted coding-agent subset is constructed)

### Common Mistakes in Month 4 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Scoring only final outputs** | It's simpler and gives you a single number | Always score the trajectory too. An agent that "stumbles into" the right answer is unreliable. |
| **Building a taxonomy you never use** | Categorizing failures is satisfying but doesn't help unless you act on it | Every entry in the taxonomy should lead to a prioritized fix. Sort by frequency × severity. Fix the top one. |
| **Ignoring compounding error** | It's counterintuitive that 95% reliable steps produce only 60% reliability over 10 steps | Calculate it. Display it. Let it guide your architecture decisions (fewer steps = more reliable). |
| **Over-engineering the eval before having enough data** | You build a complex scoring system before you have enough failure examples | Start simple: log everything, look at 50 traces by hand, label the obvious patterns. Sophistication comes from data, not from code. |

</details>

---

## Month 5 - Multi-Agent Systems & Orchestration

**What you are building:**

Extending your single agent into a multi-agent system: a Planner agent that decides what to do, a Coder agent that writes the code, and a Reviewer agent that checks the work - all coordinated as a state machine with explicit handoffs.

**Why multi-agent?**

Some tasks genuinely benefit from specialization. A large model for planning + a smaller model for execution can be both better and cheaper. But multi-agent adds complexity and failure modes - so you must prove it actually helps.

**The real 2025–2026 consensus (read both sides):**

Anthropic's multi-agent research system beat single-agent Opus by ~90% on internal breadth-first research tasks - *but burned ~15× the tokens of a chat turn*. Cognition's "Don't Build Multi-Agents" argues the opposite for coding: parallel sub-agents make conflicting implicit decisions, so a single-threaded agent that shares full context wins. The reconciliation isn't "multi-agent good/bad" - it's **task-shape-dependent**: multi-agent wins for read-heavy, parallelizable, breadth-first work where sub-agents return condensed summaries; it loses for write-heavy, tightly-coupled work (like coding) that needs shared state. Your coding agent is squarely in the second camp, which is exactly why your baseline comparison matters.

**What you will learn:**
- Orchestration patterns: orchestrator-worker, sequential/parallel handoffs, shared state vs message-passing
- The 2026 framework landscape: LangGraph (production standard for stateful workflows), OpenAI Agents SDK (good for GPT-centric work), CrewAI (fast prototyping), Google ADK (GCP-native), AutoGen/AG2 (research/conversational)
- State machines and graphs for agent coordination
- The discipline of keeping a single-agent baseline to prove multi-agent is worth the complexity

**What "done" looks like:**
- A multi-agent `banana`: Planner → Coder → Reviewer with shared state and explicit handoffs
- The Reviewer runs on a different/smaller model and must approve before the diff reaches you
- **Benchmarked against the Month 3 single-agent baseline** on the same task suite
- Honest results: multi-agent often loses on latency for simple edits. Say so if it does. Show where it genuinely wins.

**Your three numbers:**
- **QUALITY:** End-to-end completion vs the single-agent baseline
- **COST:** Added steps and tokens from coordination
- **LATENCY:** Coordination overhead measured

**Portfolio artifact:**

A tech-radar entry: *"Agent frameworks + per-agent model sizing - what we standardize on and why."*

**Reading list:**
- Anthropic - "How we built our multi-agent research system" (where multi-agent wins, and the token cost)
- Cognition (Walden Yan) - "Don't Build Multi-Agents" (why single-threaded + shared context often wins)
- LangGraph docs (the stateful-workflow framework recommended for the build)

### Common Mistakes in Month 5 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Multi-agent cargo-culting** | "More agents = better" is appealing but wrong. Anthropic's own multi-agent system cost ~15× the tokens of a single chat turn; Cognition argues parallel coding sub-agents actively make conflicting decisions. | Split only when a single agent measurably can't do the job *and* the work is parallelizable/read-heavy. Keep the baseline. Every new agent multiplies nondeterminism and token cost. |
| **Picking a framework based on hype** | Every framework has passionate advocates | Build deeply in one (LangGraph recommended for production). Be able to articulate *why* you'd pick each for specific use cases. |
| **Losing the single-agent baseline** | Once you build multi-agent, you forget to compare | Always run the same tasks on both architectures. Report the delta honestly - sometimes simpler wins. |
| **Shared state as a dumping ground** | Agents stuff everything into shared state, making debugging impossible | Design the state schema carefully. Every field should have a purpose. Log state transitions. |

</details>

---

## Month 6 - Agent Reliability Engineering & Human-in-the-Loop

**What you are building:**

Making your agent survive real-world failures - crash recovery, idempotent operations, graceful degradation, and a proper human-in-the-loop workflow with audit trails.

**Why this matters:**

This is the gap that gets agent projects cancelled. Gartner expects **>40% of agentic AI projects to be scrapped by end of 2027** - and weak reliability/risk controls are a named cause. A demo agent that works once on the happy path is not a system. Making it survive crashes, recover state, and keep humans safely in control is what separates a demo from a product.

**Go deep on two; be aware of the rest.**

This is a spike month. The two mastery targets are: (1) **crash recovery** - checkpoint/resume plus idempotent re-application, proven by a *measured* recovery-success-rate after induced kills - and (2) **human-in-the-loop** - a real approval workflow with audit logging, interruption, and resume (not a Y/N popup). The rest is *awareness*: borrow **durable-execution** ideas from Temporal as concepts, don't build a workflow engine; and wire a basic **graceful-degradation** fallback but save the serious fallback work for the outage test in Month 9 and the cost router in Month 10. When the month runs long, the recovery number and the audit trail are what must ship.

**What you will learn:**
- Checkpoint/resume: save agent state so it can recover from crashes mid-task
- Idempotent tool calls: re-applying an edit must be safe (not apply it twice)
- Graceful degradation: if the main model goes down, fall back to a smaller model or an API
- Human-in-the-loop design: approval gates that log every decision for audit, interruption and resume
- Durable execution concepts (inspired by Temporal): making long-running agent workflows reliable

**What "done" looks like:**
- Kill the agent mid-task → restart → it recovers state and pending diffs
- Re-apply an edit → it's safe (idempotent)
- Model outage → automatic fallback to a backup model
- Every risky action (file edits, shell commands) gated on human approval with audit logging
- Recovery success rate measured after induced kills

**Your three numbers:**
- **QUALITY:** Task completion rate + trajectory eval pass rate
- **RELIABILITY:** Recovery success rate after induced kill/outage (a number)
- **LATENCY:** p95 including checkpoint overhead

**Portfolio artifact:**

An *"Agent Reliability Checklist"* - a reusable standard: recovers from kill? idempotent? trajectory-scored? approval-gated?

### Common Mistakes in Month 6 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **The "demo agent" trap** | It works perfectly in your demo, so you think it's done | Kill it mid-task. Disconnect the network. Feed it malformed input. If it doesn't recover gracefully, it's not production-ready. |
| **No replay capability** | You can't reproduce a failure because you didn't save enough state | Log complete trajectories. You should be able to replay any past run step by step. |
| **Treating HITL as a simple popup** | "Press Y to continue" is not a human-in-the-loop system | Design a proper approval workflow: show the diff, explain the risk, log the decision, allow interruption and resume. Make it auditable. |
| **Ignoring checkpoint overhead** | Checkpointing adds latency, and you don't measure how much | Include checkpoint time in your p95 latency measurements. Optimize if it's too slow, but never skip it. |

</details>

---

## Month 7 - MCP & A2A: Making the Platform Agent-Agnostic

**What you are building:**

Exposing your agent's tools via MCP (Model Context Protocol - the standard for connecting AI to tools and data) and evaluating a *second, external* agent you didn't build using your harness.

**Why this matters:**

MCP is the de-facto 2026 standard. Both MCP and A2A are now under the Linux Foundation's Agentic AI Foundation. Protocol fluency is ahead of most job descriptions. And making your evaluation harness work on *any* agent (not just yours) is what converts "I built a thing" into "I can evaluate *the field's* things."

**What you will learn:**
- MCP: the standard for agent-to-tool communication (how agents connect to data and tools)
- A2A: the standard for agent-to-agent communication (how agents discover and delegate to each other)
- How to expose your tools (`read_file`, `grep`, `propose_edit`, `run_tests`) as an MCP server
- How to make your eval harness agent-agnostic - it should produce eval + trajectory + telemetry for any agent

**What "done" looks like:**
- `banana`'s tools exposed as an MCP server - verified by connecting another MCP client (e.g., Claude Desktop)
- Your eval harness successfully evaluating a second agent you didn't build (an off-the-shelf MCP-driven agent)
- Same eval + trajectory + telemetry output regardless of which agent is being tested

**Your three numbers:**
- **QUALITY:** Eval scores for your agent vs the external agent on the same tasks
- **PORTABILITY:** Number of MCP clients successfully connecting to your tools
- **GENERALITY:** Same harness producing valid results for both agents

**Portfolio artifact:**

*"I evaluated an agent I didn't build"* - the generality proof + an MCP explainer blog post.

### Common Mistakes in Month 7 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Building a custom protocol when MCP exists** | "I'll design my own tool interface" feels more engineering-like | Use MCP. It's the standard. Your tools should be reusable by any MCP client. |
| **Coupling the harness to one agent** | It's easier to hardcode assumptions about your own agent | Design the eval interface so it only depends on traces and tool calls, not on internal agent state. |
| **Ignoring A2A** | MCP gets more attention, so A2A feels optional | At minimum, understand what A2A does and when you'd use it. Agent-to-agent delegation is a real production pattern. |
| **Not testing with a real external client** | "It should work" is not the same as "it does work" | Verify with at least one real MCP client. Claude Desktop is the easiest test. |

</details>

---

# PHASE 3 - PRODUCTION & PERFORMANCE (Months 8–11)

*Goal: Make the agent fast, cheap, safe, and deployable.*

---

## Month 8 - Inference Optimization (Local)

**What you are building:**

Making your agent *fast*. Adding speculative decoding, quantization-aware quality checks, and caching - all tuned to your local hardware's memory budget (unified RAM on Apple Silicon, dedicated VRAM on an NVIDIA GPU, or system RAM on CPU).

**What you will learn:**
- Latency vs throughput: what matters for an interactive coding assistant (time-to-first-token, time-to-first-diff)
- Quantization: GGUF Q4/Q5/Q6, MLX 4-bit - what it saves, what it costs in quality
- Speculative decoding: using a small "draft" model to speed up a large model (a real win on local hardware). **Effectively GPU/Apple-only** - CPU learners won't see a meaningful local speedup, so *observe* it via a one-off cloud-GPU rental or Colab (the same one-time cloud comparison this month already prescribes) and make the quantization-frontier + caching labs your primary wins. The reasoning transfers even when your local numbers are small
- KV cache management: how to avoid recomputing context unnecessarily
- Prompt caching and semantic caching for repeated patterns

**What "done" looks like:**
- Speculative decoding implemented (small draft model + large main model) on GPU/Apple - **or**, on CPU, *observed* on a rented cloud GPU/Colab with quantization-frontier + caching as your demonstrated local wins instead
- Quantization tested at multiple levels with quality impact measured on your eval suite
- **Tool-call reliability re-checked after quantization** - quantization can degrade structured-output/schema adherence even when the overall eval score looks flat, so re-measure the Month 3 parse+validate rate at every level, not just answer quality
- Semantic cache for repeated retrieval/prompts reducing redundant computation
- **Re-run your Month 2 eval after every change** - quality must not drop

**Your three numbers:**
- **LATENCY:** p50/p95 before → after (and time-to-first-diff)
- **THROUGHPUT:** Tokens/sec per model tier, swept across 1 → N concurrent requests (a first taste of the under-load p95 you formalize into SLOs in Month 11)
- **QUALITY:** Eval score held after every optimization (non-negotiable)

**Portfolio artifact:**

A *"Local Inference Optimization Playbook"* - levers ranked by ROI for an interactive coding agent.

### Common Mistakes in Month 8 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Quantizing without re-evaluating** | "Q4 is close enough" without actually measuring | Run your full eval after every quantization level. Some coding tasks are very sensitive to quality drops. |
| **Optimizing blind** | You optimize whatever feels slow without profiling | Measure where time and memory actually go first. Profile before optimizing. |
| **Ignoring memory pressure** | You exceed your memory budget and everything slows down (SSD-swap on Apple/CPU) or fails (OOM / CPU-offload on a GPU) | Monitor peak memory usage. If model + KV cache + application exceeds available memory, you'll get worse results than a smaller model that fits. |
| **Skipping the cloud comparison** | You only test locally and never know how your numbers compare | Rent a GPU once, run the same workload on vLLM, and report the crossover point. It's one benchmark, not a lifestyle. |

</details>

---

## Month 9 - Safety, Security & Guardrails

**What you are building:**

Protecting your agent from attacks - especially indirect prompt injection (malicious instructions hidden in code repositories) - and building a red-team test suite to prove the protections work.

**Why this matters:**

A coding agent with shell access that reads untrusted repositories is a remote-code-execution hazard. This isn't theoretical: **EchoLeak (CVE-2025-32711)** was a *zero-click* indirect-injection exfiltration in Microsoft 365 Copilot (Microsoft rated it 9.3/critical); **Invariant Labs' GitHub MCP "toxic agent flow"** showed a malicious public-repo issue hijacking an agent into leaking private-repo data; and **tool poisoning** (hostile instructions hidden in an MCP tool's *description*) is a documented class. OWASP now ships the relevant catalogs: the **Top 10 for LLM Applications (2025)**, the **"Agentic AI - Threats and Mitigations" (v1.0, 2025)** threat-model guide, and the new **OWASP Top 10 for Agentic Applications (2026)**. Know all three.

**Go deep on two; be aware of the rest.**

This is a spike month. The two mastery targets are: (1) **defending against indirect prompt injection** - sandbox the shell, gate risky actions, and *prove* it with a red-team suite and a measured guardrail block-rate - and (2) **secret/PII scanning on both surfaces** (the diff path *and* the trace write path). The rest is *awareness*: use the three OWASP catalogs as a **checklist and shared vocabulary**, not something to memorize; study **EchoLeak** and the **GitHub MCP toxic-flow** as worked examples so you can recognize tool-poisoning and boundary attacks as a *class*; and treat the outage/fallback test as a re-exercise of the Month 6 mechanism, not new ground. When the month spikes, the block-rate and the redaction proof are non-negotiable; the catalog reading can stay at awareness depth.

**What you will learn:**
- OWASP Top 10 for LLM Applications (2025) and OWASP Top 10 for Agentic Applications (2026): the industry-standard threat catalogs
- Indirect prompt injection: a malicious README, code comment, or test file that tells the agent to run shell commands, exfiltrate data, or bypass safety - study EchoLeak and the GitHub MCP flow as concrete worked examples
- Tool authorization and least privilege: sandbox the shell, block network access, restrict file paths
- Secret & PII scanning on *two* surfaces: never let the agent commit secrets (API keys, passwords) in diffs, **and** never let secrets/PII it reads land in your trajectory logs/traces (you build the full redaction + retention story in Month 13)
- How to evaluate your own guardrails: guardrail block-rate as a measured metric

**What "done" looks like:**
- A red-team test: plant a malicious instruction in a code comment telling the agent to run a dangerous command → show the guardrail + approval gate blocks it
- A model outage test: induce an outage → show fallback to a smaller/backup model works
- Shell sandbox locked down: path allowlist, no network, audited approval gate
- Secret scanning on every diff before applying - *and* on the trajectory-logging path (plant a secret the agent reads → confirm it's redacted before it's written to a trace)
- Guardrail block-rate reported as a number

**Your three numbers:**
- **QUALITY/RELIABILITY:** Guardrail block-rate on injection tests (100% target)
- **SECURITY:** Zero unsandboxed shell executions, zero secrets in diffs *or* in stored traces
- **DEGRADATION:** Fallback model quality on the eval suite during outage

**Portfolio artifact:**

*"Defending an agent against indirect prompt injection"* - with the red-team demo. (This single post punches above its weight in interviews.)

**Reading list:**
- OWASP Top 10 for LLM Applications (2025) + OWASP Top 10 for Agentic Applications (2026)
- OWASP "Agentic AI - Threats and Mitigations" (v1.0)
- Aim Labs - "EchoLeak" write-up (CVE-2025-32711) and Invariant Labs - "GitHub MCP vulnerability"

### Common Mistakes in Month 9 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Security as afterthought** | "I'll add security later, let me get the features working" | A coding agent with unsandboxed shell and file access is an RCE vulnerability from day one. Sandbox first. |
| **Only testing against known attacks** | You test the 3 injection patterns you can think of | Use OWASP's frameworks systematically. Plant injection in different locations (comments, docstrings, READMEs, test files, dependency descriptions). Think like an attacker. |
| **Un-evaluated guardrails** | "We have a guardrail" without measuring if it actually works | Treat guardrails like any other system: measure them. Report block rate. Test false positives (legitimate code that looks suspicious). |
| **Trusting tool output** | The agent trusts whatever a tool returns without validation | Treat all tool outputs as untrusted input. An attacker could poison a tool's response. |

</details>

---

## Month 10 - Cost-Aware Model Routing

**What you are building:**

A smart routing layer that sends easy tasks to small/cheap/local models and hard tasks to large/expensive/cloud models - automatically, based on confidence and eval signals.

**Why this matters:**

Routing is *one of* the primary levers for agent cost in 2026 - but not the only one, and often not the biggest. Agents are dominated by large, repeated prefixes (system prompts, tool definitions, retrieved context), so **prompt caching** can dwarf routing savings: Anthropic charges 1.25× to write a cache entry and only **0.1× to read it**; OpenAI applies up to a **~90% discount** on cached input automatically. The full cost toolkit is **routing + prompt caching + context/token reduction + batch APIs**. The skill is knowing which lever applies to which workload - and proving each one held quality.

**What you will learn:**
- Routing cascade design: small model → try → evaluate confidence → escalate if needed
- When local/open models are good enough and when you need frontier (with numbers, not opinions)
- Semantic and prompt caching to avoid redundant expensive calls
- Cost attribution: knowing exactly what each step costs and where the money goes

**What "done" looks like:**
- A routing cascade: small model handles simple edits, large model handles complex planning
- Routing decisions based on confidence/eval signals (not random)
- Routing also gated on **tool-call reliability**, not just answer quality - a cheaper small model that emits malformed tool calls fails the gate even when its prose looks fine (small models regress here first)
- Cost-per-task dropped *with quality held on the eval* (non-negotiable)
- A documented "when local wins / when we route to frontier" rule with actual numbers

**Your three numbers:**
- **COST:** Cost-per-task before → after routing
- **QUALITY:** Eval score held after routing (no regression)
- **LATENCY:** p95 before → after

**Portfolio artifact:**

*"A model-routing playbook: cutting agent cost X% without dropping quality, with the eval to prove it."*

### Common Mistakes in Month 10 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Over-indexing on local models** | "Everything should run locally" is a philosophical position, not an engineering one | Local is great for privacy and cost; frontier is still better for hard tasks. Route based on data, not ideology. |
| **No quality check after routing** | You cut costs but don't verify quality held | Re-run the full eval after every routing change. A cost cut that drops quality is not an optimization - it's a regression. |
| **Routing by task type instead of confidence** | "All code edits go to the small model" is too coarse | Route by evaluated confidence on the actual output. Some "simple" tasks are surprisingly hard for small models. |
| **Ignoring cache hit rate** | You build a cache but never measure how often it actually helps | Track and report cache hit rate. A cache with a 2% hit rate is just overhead. |

</details>

---

## Month 11 - Productionize & The Justified Customization Decision

**What you are building:**

Packaging your system for distribution, adding CI/CD with eval gates, defining SLOs, and making the *calibrated* decision about whether to fine-tune a model.

**Why fine-tuning is demoted to an optional sub-task:**

In 2026, fine-tuning for its own sake is a named anti-pattern. Most teams that fine-tune should have fixed their retrieval or prompts first. Fine-tuning is what you reach for *after* retrieval + prompting + routing have plateaued - and only for narrow, well-defined tasks.

**What you will learn:**
- Packaging and distribution: making your tool installable (pip install or similar)
- **Containerize and deploy a real slice**: wrap one meaningful path of `banana` (e.g., the eval-runner API or the agent endpoint) in a Docker image and ship it to a *publicly reachable* URL. Stay provider-neutral - **Cloud Run, Fly.io, or a small VM** are all fine; pick by cost and familiarity, not lock-in. To keep this hardware-agnostic, **route the model through an API** here (the deployed box runs your Python, not a local GPU) - the point is to learn the deploy/runtime boundary, not to serve weights from a container
- CI/CD with quality gates: your eval suite runs on every PR and blocks regressions
- SLOs (Service Level Objectives): defining a quality floor, error rate, and latency budget
- Load testing: measuring p95, throughput, and error-rate under *concurrent* requests (Locust / k6 / an async batch driver) - the p95 that matters is under contention, not single-user, and local serving saturates fast
- The fine-tuning decision framework: when to fine-tune, when not to, and how to defend your choice with numbers
- If you fine-tune: LoRA on a narrow task (e.g., making a small model reliably emit your exact diff format), with training data curated from your eval failures. **The platform-neutral default is a managed cloud LoRA fine-tune** (any hosted fine-tuning service - e.g., Together, Fireworks, or a cloud provider's managed tuning), so no specific local accelerator is required. The on-device toolchains - `mlx-lm` on Apple, Unsloth/PEFT/axolotl on an NVIDIA GPU - are the hardware-specific *fast lanes*, not prerequisites; CPU-only learners use the managed path or a Colab/Kaggle GPU session

**What "done" looks like:**
- `banana` is installable with one command
- **A containerized slice is deployed and reachable at a public URL** (Cloud Run / Fly.io / small VM), with the model API-routed and secrets supplied as runtime config, never baked into the image. A `Dockerfile` + one-command deploy is documented and reproducible from a clean checkout
- CI/CD pipeline with eval gate that blocks quality regressions
- A small load test run **against the deployed endpoint** (not just localhost): p95 / throughput / error-rate measured across concurrent requests, with the **saturation point** identified (the concurrency where p95 breaks the SLO)
- SLOs defined against the *under-load* numbers - interactive p95, error rate, quality floor - not single-user best-case
- **Either** a shipped, measured LoRA fine-tune **or** a defended "we didn't need to fine-tune - here's the number" decision
- If fine-tuning: eval score before → after on held-out data, with cost comparison vs prompting the big model

**Your three numbers:**
- **QUALITY:** SLO attainment under load
- **RELIABILITY:** CI blocks a real quality regression (demonstrated)
- **CUSTOMIZATION:** Before → after numbers if fine-tuning, or the "not needed" number if not

**Portfolio artifact:**

A *production-readiness checklist* + a decision record *"Why we did/didn't fine-tune."*

### Common Mistakes in Month 11 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Fine-tuning as first resort** | "Let me fine-tune a model" feels sophisticated | Ask: "Have I tried fixing retrieval? Have I tried better prompts? Have I tried routing?" Fine-tune only when all three plateau. |
| **"Works on my laptop" deployment** | You test in one environment and hope it works everywhere | Package it properly. Test the install on a clean machine. Document dependencies. Better: deploy the container to a public URL and prove it runs off your laptop entirely. |
| **Secrets baked into the image** | It's the fastest way to make the container "just work" | API keys and tokens are runtime config (env vars / platform secrets), never layers in the image. A pushed image is effectively public - treat anything in it as leaked. |
| **SLOs without alerts** | You define quality floors but never know when they're breached | Wire up alerts. An SLO you can't monitor is a wish, not an objective. |
| **Single-user SLOs** | You measure p95 one request at a time and call it your latency budget | Local serving saturates fast. Measure p95 under concurrent load and set the SLO against *that* - a single-user p95 is a best case you'll rarely see in production. |
| **The ML-research rabbit hole on fine-tuning** | You spend weeks on hyperparameter tuning and ablation studies | Cap the fine-tuning effort. Data quality > hyperparameters. Ship one adapter with a number and move on. 500 great examples beat 50,000 mediocre ones. |

</details>

---

# PHASE 4 - THE EVALUATION PLATFORM (Months 12–14)

*Goal: Transform your tool suite into a platform that can evaluate and harden any agent, not just yours.*

---

## Month 12 - The Agent Evaluation Platform

**What you are building:**

Consolidating everything you've built (eval harness, trajectory eval, error-analysis viewer, observability, reliability, MCP support) into a coherent platform with a clean architecture and clear boundaries.

**Why this phase exists separately:**

Up to now, you've been building tools for yourself. Now you package them as a platform that could evaluate *any* agent. This is the shift from "I built an agent" to "I can make *any* agent production-ready" - which is the statement that gets you hired.

**What you will learn:**
- Platform architecture: clean component boundaries, data flows, extension points
- System integration: finding and fixing the bugs that live at the seams between components
- The "agent-agnostic" design principle: your platform should work on agents built by anyone, using any framework

**What "done" looks like:**
- A documented architecture with clear component boundaries
- All components (eval engine, trajectory eval, data viewer, observability, reliability, safety, routing) working as one integrated system
- The system tested on at least 2 different agents (your coding agent + one external agent)
- Integration seam bugs found and fixed

**Your three numbers:**
- **QUALITY:** End-to-end eval passing on both agents
- **INTEGRATION:** Number of cross-component bugs found and fixed
- **GENERALITY:** Same platform, two different agents, same quality of output

**Portfolio artifact:**

Architecture document with data flow diagrams.

### Common Mistakes in Month 12 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Adding new features instead of integrating** | "One more feature" is more fun than fixing integration bugs | Resist. This month is about making what you have work *together*. No new capabilities. |
| **Skipping the seam bugs** | Integration testing is tedious | The bugs live where eval meets observability meets routing meets safety. Hunt them deliberately. |
| **Coupling components that should be independent** | It's faster to let components share internal state | Use clean interfaces. Each component should be replaceable without breaking others. |

</details>

---

## Month 13 - Observability & Telemetry Layer

**What you are building:**

Productionizing the lightweight tracing you've emitted since Month 3 into a real observability layer - migrating your homegrown spans onto OpenTelemetry → Langfuse so you can see exactly what happened, what it cost, how long it took, and where things went wrong. Plus drift detection and a dashboard anyone can read. You are *upgrading* an existing trace stream, not adding tracing for the first time.

**What you will learn:**
- OpenTelemetry for AI: adopt the GenAI semantic conventions for the spans you've been emitting since Month 3 (thought/tool-call/result), with cost and latency attribution per step. Note the **conventions (`gen_ai.*`) are still experimental/in-development** in 2026 - adopt them, but pin versions and expect the schema to shift. The migration is mechanical because your Month-3 format already captures the right fields
- Self-hosted observability with Langfuse (runs locally via `docker compose up`, fits the privacy story). **Docker is a soft prerequisite here** - stand up the Langfuse stack from a provided docker-compose so non-DevOps learners aren't blocked; anyone who can't run Docker locally uses a small free-tier hosted Langfuse instead
- **Trace data governance**: redacting secrets/PII *before* spans are persisted, plus a retention policy (how long traces live) and access control (who can read the trace store). Your traces contain source code and can contain customer data - the local-first privacy story only holds if the trace store is actually governed
- Drift detection: automatically alerting when agent quality or behavior changes over time
- Dashboard design: a dashboard a non-engineer can read - "is the agent healthy, cheap, fast?"

**What "done" looks like:**
- Every agent run produces full traces (your Month-3 spans now flowing through OpenTelemetry → Langfuse)
- Any past run is fully reconstructable from traces - the replayability you had since Month 3, now backed by a queryable store
- Cost and latency attributed per step in the trace
- Secret/PII redaction on the trace write path - a planted secret never reaches the stored trace (the Month 9 scanner, now wired onto the telemetry pipeline), with a documented retention + access policy for the trace store
- A drift alert fires on an injected quality regression
- A dashboard showing quality, cost, latency, and drift over time

**Your three numbers:**
- **OBSERVABILITY:** % of runs with complete traces (target: 100%)
- **COST ATTRIBUTION:** Cost attributed to {task, step, agent} level
- **DRIFT:** Time from injected regression to alert firing
- **GOVERNANCE:** Zero secrets/PII in stored traces (verified by a planted-secret test); retention + access policy documented

**Portfolio artifact:**

Dashboard screenshots + *"What to put on an agent observability dashboard (and what's noise)."*

### Common Mistakes in Month 13 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Logging everything and surfacing nothing** | It's easier to log than to decide what matters | Every metric on the dashboard should correspond to a decision you'd make. If a number going up or down doesn't change what you do, remove it. |
| **Vanity dashboards** | Impressive-looking charts that don't help anyone | Ask: "What question does this chart answer? What action does the answer drive?" If you can't answer both, cut the chart. |
| **Missing cost attribution** | You know the total cost but not where the money went | Attribute cost to the task/step/agent level. This is what makes routing decisions data-driven. |
| **Secrets and PII in your traces** | Full-trajectory logging captures whatever the agent read - including secrets and customer data | Redact on the *write* path, before anything is persisted. Set retention and access controls. A trace store full of plaintext secrets is its own breach waiting to happen. |

</details>

---

## Month 14 - Advanced Reliability & Second System-Under-Test

**What you are building:**

Hardening the platform with a second, *real-world* system-under-test - proving the platform generalizes by evaluating an agent you didn't build, end-to-end, through all your layers.

**What you will learn:**
- Real-world generalization: does your platform actually work on someone else's agent?
- Advanced failure modes: failures you've never seen because your own agent doesn't trigger them
- The complete "demo to production" narrative: quantifying how your platform improved an agent's reliability

**What "done" looks like:**
- A second external agent evaluated end-to-end through your platform
- Reliability, safety, and quality numbers for the external agent
- A "demo → production" delta: before/after reliability numbers showing what your platform contributed
- New failure modes added to your taxonomy from the external agent's behavior

**Your three numbers:**
- **QUALITY:** External agent's eval score through your platform
- **RELIABILITY:** Recovery and safety scores for the external agent
- **DELTA:** Measured improvement from demo to production-grade

**Portfolio artifact:**

A case study *"How we took an agent from demo to production - with numbers."*

### Common Mistakes in Month 14 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Only testing agents you built** | Your own agent has learned to avoid your harness's blind spots | Use a genuinely external agent. The failures it triggers will teach you things your own agent never could. |
| **Not updating the taxonomy** | New failure modes from the external agent don't get categorized | Treat every new failure as a taxonomy update. Your taxonomy should grow whenever you encounter a new type of failure. |
| **Overfitting the platform to your agent** | Implicit assumptions about your agent's behavior baked into the platform | Test with agents that use different tool schemas, different step counts, different models. Generality must be proven. |

</details>

---

# PHASE 5 - LEADERSHIP & CAPSTONE (Months 15–18)

*Goal: Turn your platform into something others can build on, write the documents that demonstrate senior judgment, and tie everything together.*

---

## Month 15 - The Paved-Road Platform SDK

**What you are building:**

A plugin/extension system so other engineers can add new tools, new agents, or new eval criteria to your platform - and automatically inherit your eval, observability, safety, and reliability layers for free.

**Why this matters:**

The highest-leverage work is the reusable platform that lets ten engineers ship safely - not the one app you build yourself. Making the safe, evaluated, observed path the *easy default* is the definition of platform thinking.

**What you will learn:**
- SDK and plugin design: making it easy for someone to add a new tool or agent without touching the core
- Developer experience: docs, starter templates, sensible defaults, escape hatches
- "Paved road" principle: the right way should be the easiest way

**What "done" looks like:**
- A plugin SDK that lets someone add a new tool or a new agent to the platform
- The new tool/agent automatically inherits eval + observability + safety guardrails
- **Proof:** at least one real extension pulled through the SDK (you or a colleague adding a new tool in under 1 day)
- Documentation and a starter template

**Your three numbers:**
- **TIME:** Time-to-first-evaluated-extension for a new user - or your self-timed cold walkthrough (target: < 1 day)
- **COVERAGE:** % of platform capabilities with default eval
- **ADOPTION:** The extension is working and tested

**Portfolio artifact:**

The SDK published as an open-source package.

### Common Mistakes in Month 15 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **A platform nobody uses** | You build it in isolation without testing with real users | Pull one real extension through the SDK before calling it done. If it takes more than a day, the SDK needs work. |
| **Premature platforming** | You try to make everything generic before it works specifically | This works because you've extracted from 14 months of real building. The abstractions are earned. |
| **Over-engineering the extension points** | "What if someone needs to..." for every possible future use case | Design for the use cases you've actually seen. Add extension points when someone actually needs them, not before. |

</details>

---

## Month 16 - Technical Leadership Artifacts

**What you are building:**

The written artifacts that demonstrate senior-level judgment - design documents, tech radars, and a recorded tech talk. The code is done; now you prove you can *lead* with what you've built.

**What you will learn:**
- Writing that decides things: RFCs, Architecture Decision Records (ADRs), the one-page recommendation both a busy executive and a hands-on engineer trust
- Tech radar: a structured opinion on what to adopt/trial/assess/hold in the AI agent stack
- The art of calibrated honesty: "this doesn't need an agent," "local can't do this yet," "we shouldn't fine-tune here" - each with a number
- Presenting to a hostile audience: defending your decisions against "why not just use the frontier model for everything?"

**What "done" looks like:**
- A **design doc/RFC**: *"An agent evaluation & reliability platform - where it wins, where it doesn't, the security model"*
- A **tech radar**: model selection, framework choices, build-vs-buy decisions, all with your measured numbers from Months 5/8/10
- A **recorded ~15-minute tech talk**: "Eval-driven development for agents" or "Defending agents against prompt injection"
- A **hostile review session**: someone attacks your RFC ("why not just buy Braintrust?") - you defend with numbers and revise the doc

**Your three numbers:**
- **REVIEW:** Design doc reviewed and revised - against a peer, or against the self-administered question bank
- **TALK:** Tech talk recorded and published
- **DEFENSE:** One decision defended under hostile Q&A (including "why local at all?")

**Portfolio artifact:**

The RFC + tech radar + recorded talk - all public.

### Common Mistakes in Month 16 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **"Senior = more code"** | Writing feels like "not real work" | At this level, decisions and other people's leverage are your primary output. The bottleneck is judgment and communication, not more code. |
| **Writing only for engineers** | Your design docs are incomprehensible to non-technical stakeholders | Write so both a busy executive and a hands-on engineer can understand the tradeoffs. Use the Pyramid Principle: conclusion first, then supporting evidence. |
| **Avoiding the hostile review** | Getting challenged is uncomfortable | Seek out the hardest questions. A design that survives hostile review is 10x more credible than one nobody questioned. |
| **Perfectionism on the talk** | "I need to practice 20 more times" | Record it when it's good enough. Ship it. A published 85%-polished talk creates infinitely more signal than an unpublished perfect one. |

</details>

---

## Month 17 - Portfolio Polish & Open-Source Contribution

**What you are building:**

Your public presence - the visible body of work that hiring managers, colleagues, and the community can see. Plus meaningful contributions to the open-source tools you've used all year.

**What you will learn:**
- How to tell a coherent technical story (from agent → eval → platform)
- Open-source contribution etiquette: meaningful PRs to projects you actually use (Phoenix, Langfuse, promptfoo, LangGraph, MCP SDKs)
- Public writing that gets shared: opinionated field notes with numbers, not tutorials

**What "done" looks like:**
- A polished public repository with a killer README: architecture diagram, headline numbers, 90-second demo video
- 6–8 blog posts published (the ones you've been writing throughout), cross-posted
- At least 3 meaningful open-source PRs **opened and engaged** (to eval/observability/agent tools you used). *Opened + engaged* is the deliverable you control: a real PR submitted, CI green, and you responsive in the review thread. **Merge is the bonus, not the bar** - maintainer timelines are outside your control, so a slow review must never block the month
- A polished LinkedIn/personal-site presence linking to all of the above

**Your three numbers:**
- **PORTFOLIO:** Complete public repo + README + demo video
- **WRITING:** 6+ posts published
- **OSS:** 3+ PRs opened + engaged on external projects (merged = bonus)

**Portfolio artifact:**

The complete public portfolio - repo + blog + OSS trail + talk.

### Common Mistakes in Month 17 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Invisibility** | "The work should speak for itself" | It doesn't. Publish, document, give the talk. The most common failure mode of talented engineers is that nobody knows what they did. |
| **Tutorial-style writing** | "How to set up Langfuse" is easier to write than "What we learned from 500 agent failures" | Write opinionated field notes with your own numbers. Nobody needs another setup tutorial. Everyone wants real data from real systems. |
| **Spray-and-pray OSS contributions** | Fixing typos in 20 repos to pad your contribution graph | 3 meaningful PRs *opened and engaged* on projects you *actually used* is infinitely more credible than 20 typo fixes. Contribute eval examples, judge calibration recipes, integration fixes. (Merge if it lands; the substance and the review engagement are what signal, not the green badge.) |

</details>

---

## Month 18 - Capstone: Integrate, Narrate, Prove

**What you are building:**

The final integration - everything from Months 1–17 consolidated into one coherent, demonstrated, defensible system. The capstone is the proof. The discipline is: *integrate, don't invent.*

**What "done" looks like:**
- The complete `banana` platform running end-to-end: eval engine + trajectory eval + data viewer + observability + reliability + HITL + safety + routing + MCP + plugin SDK
- Tested on at least 2 agents (your coding agent + one external)
- A written architecture overview with the full data/control flow
- The headline numbers: quality, cost, latency, reliability - all honest, all with confidence intervals
- **A public, clickable demo** - a hosted URL a hiring manager can open and use in under a minute, no install required. Build on the Month 11 containerized slice: Docker → Cloud Run / Fly.io / small VM, model API-routed so it runs anywhere. Put a thin UI (or a live, authenticated API + example requests) in front of one compelling path. Treat it as a public surface - rate-limit it, cap spend, redact traces, and never expose a key (the Month 9 + Month 13 governance work earns its keep here)
- A 5-minute polished demo video (the fallback for when the live demo is down - link both)
- The complete portfolio: repo + architecture doc + blog posts + tech talk + OSS trail

**Your three numbers (consolidated):**
- **QUALITY:** Task-completion + diff-accept rate on benchmark (vs frontier API baseline - the honest gap)
- **COST:** Cost-per-task after routing and optimization (local ≈ $0 marginal - with the quality-held proof)
- **LATENCY:** Interactive p95 *under concurrent load* (the Month 11 number, not single-user best-case) + time-to-first-diff

**Portfolio artifact:**

The capstone write-up - a single document that links to everything and tells the story end-to-end.

### Common Mistakes in Month 18 - and How to Avoid Them

<details>
<summary><strong>View mistakes and fixes</strong></summary>

| Mistake | Why it happens | How to avoid it |
|---------|---------------|-----------------|
| **Scope creep** | "Just one more feature" in the final month | Resist. This month is integration and polish only. No new capabilities. |
| **Perfectionism** | "It's not ready" when it clearly is | Done = useful, measured, honest about limitations. Ship it. |
| **Not telling the honest story** | Hiding the parts where local/open models lose to frontier | The honest gap - "here's where it loses, here's the number" - is the most credible thing in your portfolio. Calibrated honesty reads as more senior than any hype. |
| **Forgetting the narrative** | You have 18 months of great work with no connecting thread | Write the story: "I built an agent. I learned to evaluate it. I learned to make it reliable. I built a platform that makes *any* agent production-ready. Here are the numbers." That's the story. |
| **A public demo that bankrupts or embarrasses you** | You expose the live demo with an uncapped key and no limits | A clickable demo is a public surface. Rate-limit per IP, set a hard spend cap on the routed model, redact traces, and keep the demo path read-mostly. The 5-minute video is your fallback when it's down. |

</details>

---

# CONSOLIDATED REFERENCE

## The Elevator Pitch

> *"I built `banana` - an agent evaluation & reliability platform that takes AI agents from demo to production. It scores trajectories (not just outputs), detects failure modes in a custom data viewer, survives crash recovery, defends against prompt injection attacks, routes across local and cloud models for cost efficiency, and works on any MCP-compatible agent - not just the one I built. I can defend every layer with a number."*

That sentence is the narrative. Every month feeds it a number.

---

## The 10 Most Valuable Skills (Where You Learn Them)

| Rank | Skill | Where you learn it | Why it's durable |
|------|-------|-------------------|-----------------|
| 1 | Error analysis - looking at the data | Months 2, 4, throughout | Models can't do this for you - you need to understand *your* data |
| 2 | Evaluation design - deciding what to measure | Months 2, 4, 8 | The harness plumbing is commoditized; the *taste* is not |
| 3 | System architecture for non-deterministic systems | Months 3, 5, 6, 12 | Compounding error reasoning doesn't change with model generations |
| 4 | Reliability engineering for agents | Months 6, 9, 14 | Gartner: >40% of agentic projects cancelled by 2027 - owning reliability is rare and valuable |
| 5 | Cost/latency/quality tradeoff judgment | Months 10, 11 | Model routing and build-vs-buy calls define seniority |
| 6 | Context engineering | Months 3, 5 | The successor to prompt engineering - managing "working memory" |
| 7 | Technical writing & influence | Months 16, throughout | Senior output is decisions expressed through writing |
| 8 | Protocol fluency (MCP / A2A) | Months 7, 12 | The industry standard - under the Linux Foundation |
| 9 | Security & safety | Months 9, 13 | OWASP LLM + Agentic Top 10 - the threat is real |
| 10 | Build-vs-buy judgment | Months 11, 15 | "Should we fine-tune? Use an agent? Buy a vendor?" - calibrated honesty |

**What is NOT on this list (commoditized or churning):**

prompt-engineering tricks, memorizing one framework's API, hand-rolling RAG plumbing, fine-tuning for its own sake, vector-DB tuning lore, chasing each new model's quirks. Learn these just-in-time as disposable scaffolding.

---

## The Mistake Catalog (All 22 Mistakes to Avoid)

These are the most common failures across the entire 18-month journey, organized by when they typically strike:

| # | Mistake | When it hits | Fix |
|---|---------|-------------|-----|
| 1 | **Vibes-based development** - "it feels better" instead of measuring | Throughout | Eval gates everything. No merge without numbers. (Month 2) |
| 2 | **Transformer math rabbit hole** - weeks on attention heads and linear algebra | Month 1 | Cap at intuition. Watch one video. Move on. |
| 3 | **Framework theology** - "LangChain vs LlamaIndex" debates instead of building | Months 1, 5 | Build deeply in one. Articulate tradeoffs. Don't marry a framework. |
| 4 | **Trusting a small local AI judge** - it hallucinates agreement more than big models | Month 2 | Always calibrate vs human labels. Report agreement rate. Prefer deterministic checks. |
| 5 | **Single-number theater** - "87% accuracy" without confidence intervals | Month 2 | Report CIs on small sets. "87% ± 12%" is honest; "87%" alone is misleading. |
| 6 | **"Agent for everything"** - using agents where a script would do | Month 3 | Before building an agent workflow, ask: "Would a deterministic script do this?" |
| 7 | **Unbounded loops** - no step/spend cap on agent runs | Month 3 | Hard limits on steps, tokens, and time. Always. |
| 8 | **Blaming the model when retrieval is broken** - "the model is dumb" | Month 3 | Measure retrieval separately from generation. Fix retrieval first. |
| 9 | **Scoring only final outputs** - ignoring the path the agent took | Month 4 | Score trajectories: right files? sensible plan? efficient tool use? |
| 10 | **Multi-agent cargo-culting** - more agents = better (no) | Month 5 | Keep the single-agent baseline. Split only when measurably necessary. |
| 11 | **The "demo agent" trap** - works once on the happy path | Month 6 | Kill it mid-task. Disconnect the network. Feed it garbage. It must survive. |
| 12 | **Building a custom protocol when MCP exists** | Month 7 | Use the standard. Don't reinvent what the Linux Foundation already standardized. |
| 13 | **Quantizing without re-evaluating** - Q4 "close enough" without measuring | Month 8 | Run full eval after every optimization. Quality must be held. |
| 14 | **Security as afterthought** - "I'll add security later" | Month 9 | A coding agent with unsandboxed shell is an RCE vulnerability. Sandbox first. |
| 15 | **Prompt injection via untrusted repo content** - trusting code files blindly | Month 9 | Treat all repo content as untrusted input. Test with planted malicious content. |
| 16 | **Over-indexing on local models** - ideology over engineering | Month 10 | Route based on data. Local for privacy/cost; frontier for hard tasks. |
| 17 | **Fine-tuning as first resort** - reaching for LoRA before fixing retrieval | Month 11 | Ask: "Have I tried fixing retrieval? Better prompts? Better routing?" Fine-tune last. |
| 18 | **A platform nobody uses** - building in isolation | Month 15 | Pull one real extension through the SDK before calling it done. |
| 19 | **"Senior = more code"** - coding instead of writing and leading | Month 16 | At senior levels, decisions and other people's leverage are your output. |
| 20 | **Invisibility** - great work that nobody knows about | Month 17 | Publish, document, give the talk. Invisibility is the most common talented-engineer failure. |
| 21 | **Scope creep in the final stretch** - "one more feature" | Month 18 | Integrate. Don't invent. Ship what you have. |
| 22 | **Hiding the honest gap** - not admitting where your system loses | Month 18 | "Here's where it loses, here's the number" is the most credible thing in your portfolio. |

---

## Technology Stack Reference

### Models & Runtimes

| Layer | What to use | Notes |
|-------|------------|-------|
| **Cloud APIs** | OpenAI, Anthropic, Google (via router) | Your quality/capability ceiling; escalation target for routing |
| **Router** | OpenRouter or LiteLLM | Abstracts provider, enables routing logic |
| **Local runtime** | Ollama (easy, cross-platform), llama.cpp (fine GGUF control, cross-platform), MLX/mlx-lm (Apple-native, fast) | Your cost/privacy arm. Pick the runtime for your hardware: Ollama or llama.cpp/GGUF run on any platform (Apple, NVIDIA GPU, CPU); MLX is the Apple-native fast path. The MLX-specific labs are optional if you're not on Apple. |
| **Coding models** | Qwen2.5-Coder (1.5B/7B/14B/32B), DeepSeek-Coder-V2 | 32B for planning; 7B for drafting |
| **Embeddings** | nomic-embed-text, bge-*, mxbai-embed-large (via Ollama) | For code retrieval |
| **Fine-tuning** | mlx-lm LoRA (Apple, on-device, 7-8B feasible); Unsloth / PEFT / axolotl (NVIDIA) | Month 11, only if justified; pick the toolchain for your hardware |

### Agent Frameworks (2026 Landscape)

| Framework | Best for | Notes |
|-----------|---------|-------|
| **LangGraph** | Production-grade, complex stateful workflows | The production standard; graph-based state management |
| **OpenAI Agents SDK** | GPT-centric, fast integration | Good if locked into OpenAI ecosystem |
| **CrewAI** | Rapid prototyping, role-based teams | Great for getting started; harder to debug at scale |
| **Google ADK** | GCP-native, multimodal workflows | Best within Google Cloud stack |
| **AutoGen/AG2** | Research, conversational multi-agent | Powerful but can be unpredictable at scale |

### Protocols

| Protocol | Purpose | Status (2026) |
|----------|---------|--------------|
| **MCP** (Model Context Protocol) | Agent ↔ Tools/Data | De facto standard, Linux Foundation/AAIF |
| **A2A** (Agent-to-Agent Protocol) | Agent ↔ Agent | v1.0, growing adoption, same governance |

### Evaluation & Observability (2026 Landscape)

| Tool | Best for | Notes |
|------|---------|-------|
| **Langfuse** | Self-hosted tracing + evals + prompt mgmt | Open-source, OTel-native - fits the local/privacy story; recommended default for the build |
| **Arize Phoenix** | Open-source OTel tracing + eval | Strong for trace-level debugging |
| **promptfoo / DeepEval** | Declarative eval harnesses | Good for patterns; don't adopt wholesale - you're building your own |
| **Braintrust** | Eval-first commercial platform | Used by Notion, Vercel, Replit, Zapier; the "buy" option you benchmark against in Month 16 |
| **LangSmith / W&B Weave / Helicone** | Commercial tracing/eval (LangChain / W&B / proxy-based) | Know they exist; pick by ecosystem fit |

> **Build-vs-buy note:** you build your own harness *to learn the judgment*, then map it onto these tools. In a real job you'd usually buy the platform and spend your time on error analysis and eval design - the parts that don't commoditize.

### Inference Serving (when you outgrow local)

| Engine | Best for | Notes |
|--------|---------|-------|
| **vLLM** | The default open-source production server | PagedAttention, automatic prefix caching, KV cache, speculative decoding, continuous batching |
| **SGLang** | High-throughput agentic / structured output | RadixAttention prefix reuse |
| **TensorRT-LLM** | Max performance on NVIDIA hardware | Fastest, but more complex to operate |
| **Ollama / MLX** | Local dev tier (this roadmap's primary arm) | Not production serving - great for learning and the cost/privacy story |

### Security Frameworks

| Framework | Scope | Key risks |
|-----------|-------|-----------|
| **OWASP Top 10 for LLM Applications** (2025) | LLM-based applications | Prompt injection, sensitive-info disclosure, supply chain, improper output handling, excessive agency, unbounded consumption |
| **OWASP "Agentic AI - Threats and Mitigations"** (v1.0, 2025) | Agent threat-modeling reference (not a ranked top-10) | Memory poisoning, tool misuse, privilege compromise, cascading failures |
| **OWASP Top 10 for Agentic Applications** (2026) | Autonomous agent systems (ranked list) | Excessive agency, tool poisoning, cascading failures |

---

## Hardware Requirements

The roadmap is organized by your **memory budget**, not your vendor. What matters is how much memory your accelerator can give the model (unified RAM on Apple Silicon, dedicated VRAM on an NVIDIA GPU, or system RAM on CPU) - pick whichever hardware you already have.

| Tier | Memory budget | Example hardware | What you can run |
|------|---------------|------------------|-----------------|
| **Minimum** | ~16 GB | Apple Silicon Mac (16GB) · NVIDIA GPU (≥8–12GB VRAM) · 16GB CPU box · a little cloud credit | 7B-14B models comfortably; routing to cloud for heavier work |
| **Recommended** | ~32 GB+ | Apple Silicon Mac (32GB+) · NVIDIA GPU (≥24GB VRAM) · 32GB+ CPU box | 32B models (Q4), small draft model concurrently, on-device LoRA |

> **You do not need a Mac to follow this roadmap.** ~90% of the work is hardware-agnostic Python + APIs (eval, trajectory eval, reliability, MCP, safety, routing, observability, the platform, the SDK, and all the leadership/portfolio work). The only hardware-specific parts - the second local backend (Month 1), the local inference optimization specifics (Month 8), and the optional fine-tune (Month 11) - each have an equal path on every platform: **Ollama/llama.cpp** for the runtime (any platform), **GGUF quantization** for the optimization work (any platform) with **MLX 4-bit** as the Apple fast-path and **AWQ/GPTQ** on a GPU, and **`mlx-lm`** (Apple) / **Unsloth/PEFT/axolotl** (NVIDIA) / **managed cloud** for fine-tuning. The *principles* (memory budgeting, the quantization frontier, speculative decoding, quality-held-after-every-change) transfer to any hardware; only the tooling and the specific numbers change.

---

## Core Reading List (Return All Year)

### Essential (Read First)
- Chip Huyen - *AI Engineering* (the spine of the whole journey)
- **Hamel Husain - "A Field Guide to Rapidly Improving AI Products"** (the single most important essay on AI eval) + "Your AI Product Needs Evals"
- **Eugene Yan - "Evaluating the Effectiveness of LLM-Evaluators (LLM-as-Judge)"**
- **"What We Learned from a Year of Building with LLMs"** (applied-llms.org)
- Anthropic - "Building Effective Agents" + "Effective Context Engineering for AI Agents"
- The multi-agent debate: Anthropic "multi-agent research system" vs Cognition "Don't Build Multi-Agents"

### Technical Reference
- Ollama, MLX/`mlx-lm`, llama.cpp docs (serving, quantization, LoRA)
- vLLM / SGLang docs (production-grade serving, prefix/KV caching, speculative decoding) - for the cloud-comparison benchmark
- MCP spec + SDK docs; A2A spec (v1.0)
- OWASP Top 10 for LLM Applications (2025) + OWASP Top 10 for Agentic Applications (2026) + "Agentic AI - Threats and Mitigations"
- OpenTelemetry GenAI semantic conventions (still experimental) + Langfuse docs
- Anthropic & OpenAI prompt-caching docs (the cost math behind Month 10)
- Sierra τ-bench + SWE-bench Verified (agent benchmarking methodology)

### Systems & Architecture
- Richards & Ford - *Fundamentals of Software Architecture* / *The Hard Parts*
- SWE-bench / SWE-bench-lite methodology

### Leadership
- Larson - *Staff Engineer*
- Reilly - *The Staff Engineer's Path*
- Minto - *The Pyramid Principle*

---

## The Portfolio Plan (What Exists at Month 18)

A single coherent, public body of work:

1. **`banana` platform** - agent evaluation & reliability platform with:
    - Instrumented multi-backend AI client (Month 1)
    - Eval harness + error-analysis data viewer + golden dataset + CI gate (Month 2)
    - Supervised coding agent as system-under-test (Month 3)
    - Trajectory eval + failure-mode taxonomy (Month 4)
    - Multi-agent system with baseline comparison (Month 5)
    - Reliability layer: checkpoint/resume, idempotency, HITL (Month 6)
    - MCP server + agent-agnostic eval (Month 7)
    - Local inference optimization (Month 8)
    - Safety & red-team suite (Month 9)
    - Cost-aware model routing (Month 10)
    - Production deployment with CI eval gates + SLOs (Month 11)
    - Integrated platform architecture (Month 12)
    - Observability + telemetry dashboard (Month 13)
    - Second agent evaluated end-to-end (Month 14)
    - Plugin SDK (Month 15)
    - Design doc + tech radar + recorded talk (Month 16)

2. **6–8 published blog posts** on the hard, durable topics:
    - "Why your AI eval is lying to you"
    - "Scoring the path, not the answer: trajectory eval"
    - "The production gap: why 40% of agent projects get cancelled (and the reliability work that prevents it)"
    - "A model-routing playbook with the eval to prove quality held"
    - "Defending an agent against indirect prompt injection"
    - "I evaluated an agent I didn't build (MCP)"

3. **1 recorded tech talk** (~15 minutes)

4. **3+ open-source PRs opened + engaged** on the tools you used (Phoenix, Langfuse, promptfoo, LangGraph, MCP SDKs) - merged is the bonus, not the bar

5. **The design doc, tech radar, and production-readiness checklist**

---

## Operating Principles (Carry Forever)

1. **Measure or it didn't happen.** QUALITY, COST, LATENCY - on everything.
2. **Eval is the bedrock.** The test suite for non-deterministic software. Everything plugs into it.
3. **Look at the data.** The highest-ROI activity in AI development. Teams that do this iterate 10x faster.
4. **Leverage over output.** The platform, the standard, the design doc, the decision - these multiply your impact.
5. **Calibrated honesty.** "Local can't do this yet - here's the number. Here's where we route to an API." That honesty is the most credible thing in your portfolio.
6. **Patterns over tools.** Models and runtimes churn; eval, retrieval, orchestration, reliability, inference economics don't.
7. **Ship and publish.** The tenth unreleased refinement compounds into nothing. Done, measured, and visible beats perfect and invisible.

---

## Month-by-Month Quick Reference

| Month | Focus | Key Deliverable | Top Mistake to Avoid |
|-------|-------|-----------------|---------------------|
| 0 | On-Ramp | Diagnostic + 50-line warm-up build + hardware track | Skipping prerequisites (they ambush you in Month 3) |
| 1 | AI Client | Multi-backend instrumented client | Transformer math rabbit hole |
| 2 | Evaluation | Eval harness + error-analysis viewer | Vibes-based development |
| 3 | First Agent | Supervised coding agent + retrieval | Agent for everything |
| 4 | Trajectory Eval | Path scoring + failure taxonomy | Scoring only final outputs |
| 5 | Multi-Agent | Planner/Coder/Reviewer + baseline comparison | Multi-agent cargo-culting |
| 6 | Reliability | Checkpoint/resume + HITL + idempotency | The "demo agent" trap |
| 7 | MCP/A2A | MCP server + agent-agnostic eval | Building custom protocols |
| 8 | Optimization | Speculative decoding + caching + quantization | Quantizing without re-evaluating |
| 9 | Security | Red-team suite + guardrails | Security as afterthought |
| 10 | Cost Routing | Routing cascade + cost attribution | Over-indexing on local models |
| 11 | Production | CI/CD + SLOs + fine-tune decision | Fine-tuning as first resort |
| 12 | Platform Integration | Architecture consolidation | Adding new features |
| 13 | Observability | Tracing + dashboard + drift detection | Logging everything, surfacing nothing |
| 14 | Generalization | Second agent evaluated end-to-end | Only testing your own agent |
| 15 | Platform SDK | Plugin system + developer docs | A platform nobody uses |
| 16 | Leadership | Design doc + tech radar + tech talk | "Senior = more code" |
| 17 | Portfolio | Blog posts + OSS PRs + polished presence | Invisibility |
| 18 | Capstone | Integration + narrative + demo | Scope creep |

> *Plus four **buffer / rest months** - one after each of Phases 1–4 - for catch-up, consolidation, rest, or adjacent self-study. See [The Cadence](#the-cadence-and-the-22-month-calendar). That's why 18 work-months run on a ~22-month calendar.*

---

*An 18-month, build-first roadmap for Applied AI Engineering. Build an agent, learn to evaluate it, learn to make it reliable, then build a platform that makes any agent production-ready. Measure everything. Publish everything. Tell the honest story - including where it loses. That's how you build the skills, judgment, and systems thinking to work on AI systems seriously.*

---
