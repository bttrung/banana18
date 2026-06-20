<div align="center">

# 🍌 banana18 🥃

**One project. 18 months. Everything public.**

[![Discord](https://img.shields.io/badge/Discord-Join_the_journey-5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/ETFrkZCtp)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](./LICENSE)
[![Contributing](https://img.shields.io/badge/Contributing-Read_the_guide-blue?style=flat)](./CONTRIBUTING.md)
![Status](https://img.shields.io/badge/Status-Month_1_of_18-orange?style=flat)

</div>

---

## 🍌 Why banana?

In 🇻🇳 Vietnam, banana wine is a traditional homemade drink. It looks simple and harmless, but it is much stronger than it seems.

After a few glasses, the room changes. People talk more, laugh more, and become much more confident than they were at the start. I have shared banana wine many times with colleagues after work. Those nights are always memorable because they bring good energy and a lot of fun after stressful working hours.

But there is one important lesson: if you drink too much, you can black out.

When I was naming this project, I wanted a name that showed what building with AI really feels like.

At first, AI feels light and easy. You try one thing, then another, and the results come quickly. Each small success makes you more confident, so you keep going.

But the more you use it, the harder it can be to notice when you are losing control. You may start depending on it too much, skipping the hard questions, or trusting outputs without fully understanding them.

And if you go too far, you can “black out.” Not in the drinking sense, but in the work sense: you lose visibility. You no longer know how decisions were made, why the system behaves a certain way, or where the risks are hiding.

That is why the name fits. Building with AI can be exciting, fun, and full of energy. But it also needs care, reflection, and respect for how powerful it can become.


🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌🍌

But maybe that is just the serious explanation.

The real answer is much simpler:

I just like drinking banana wine 😂

---

## 🧩 The Plan

This is a commitment: **18 months, one evolving project, ~10 hours per week, everything documented.**

I'm starting from scratch - no existing AI platform, no head start. The plan is to build a local AI coding assistant first, then gradually expand it into something more serious: an **Agent Evaluation & Reliability Platform** that can take any AI agent from a working prototype to something genuinely production-worthy.

---

## 🌟 Why This, and Not Something Else

There's a version of this journey where I just... build stuff. Spend 18 months chasing new models, new frameworks, new prompting tricks. It would feel productive. I'd have a lot of GitHub commits. I would not, at the end of it, be significantly better at the thing that actually matters.

The thing that actually matters in 2026 is not building AI demos. It's making AI systems work *reliably* - at a quality you can measure, at a cost you can defend, in production, every day. That's the gap between what's easy and what's valuable. And it's where most teams struggle.

So the plan is structured around two ideas that reinforce each other:

- **First**, build an agent. Not to use it, but to understand it - how it thinks, where it fails, why it fails, what "working" actually means for a non-deterministic system. You can't evaluate something you don't understand from the inside.

- **Second**, build the system around the agent. The eval harness, the reliability layer, the observability, the cost routing, the safety guardrails. The infrastructure that turns "it works when I demo it" into "it works for users, consistently, and I have the numbers to prove it."

Neither half is complete without the other. Building just the agent teaches you AI. Building just the platform teaches you infrastructure. Building both teaches you how to *ship* AI - which is the actual job.

---

## 📌 The One Rule

> **Every deliverable earns three numbers: QUALITY, COST, and LATENCY.**

Before anything gets built, before anything gets merged, before anything gets written about - it needs a number for each.

| | |
|--|--|
| 🎯 **QUALITY** | Does it work? How often? How well? |
| 💰 **COST** | What does it cost to run - in money, time, and compute? |
| ⚡ **LATENCY** | How fast is it? How long does the user wait? |

A claim without a number is just an opinion. This rule doesn't change across all 18 months.

---

## 🧭 The Shape of the Journey

The project has 5 phases. Each one builds directly on the last - nothing gets thrown away, everything accumulates.

> The month numbers below show 18 working months of banana content, spread across about 22 calendar months. 
> 
> After each phase, there is one planned buffer month with no new banana content.
> 
> These buffer months are part of the plan. They give me space if a phase takes longer than expected. They also give me time to review, rest, and prepare before starting the next phase.
> 
> If I am ahead, the buffer month becomes time for recovery, cleanup, writing, or extra study.
> 
> If I am behind, the buffer month helps me finish the current phase properly before moving on.

**Months 1–3: Foundations.** Build the instrumented AI client, build the eval harness, build the first agent. By the end of this phase, I'll have a supervised coding assistant running locally and a test suite that can measure whether it's actually working.

**Months 4–7: Agent Engineering.** Extend the single agent into a multi-agent system, add proper reliability (crash recovery, idempotent operations, human-in-the-loop), and expose everything through the MCP protocol so it can talk to other tools and agents.

**Months 8–11: Production & Performance.** Make it fast, make it cheap, make it safe. Inference optimization, cost-aware model routing, red-team testing against prompt injection attacks, CI/CD with eval gates, and the fine-tune decision - a careful, data-driven call about whether fine-tuning even helps.

**Months 12–14: The Evaluation Platform.** Consolidate everything into a coherent platform with clean boundaries. Add full distributed tracing, drift detection, and dashboards. Then prove it generalizes: evaluate an agent I didn't build, end-to-end, through all the same layers.

**Months 15–18: Leadership & Capstone.** Build the plugin SDK so other engineers can extend the platform. Write the design doc and tech radar that show the reasoning, not just the result. Record the talk. Ship the portfolio. Tie everything together.

---

## 🗓️ The Month-by-Month Plan

| Month | Focus                                    | Key Deliverable                                                                                                                          | Status                 |
|-------|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| 1     | 🔌 AI Client      | Multi-backend instrumented AI client                       | ⏳ Upcoming 01-Jul-2026 |
| 2     | 🧪 Evaluation     | Eval harness + error-analysis data viewer                        | ⏳ Upcoming 01-Aug-2026 |
| 3     | 🤖 First Agent    | Supervised coding agent + context retrieval    | ⏳ Upcoming 01-Sep-2026 |
| -     | ⏸️ Rest                                  | Buffer after Phase 1                                                                                                                     | ⏳ Upcoming 01-Oct-2026 |
| 4     | 🛤️ Trajectory Eval | Path scoring + failure-mode taxonomy | ⏳ Upcoming 01-Nov-2026 |
| 5     | 🕸️ Multi-Agent    | Planner / Coder / Reviewer pipeline                       | ⏳ Upcoming 01-Dec-2026 |
| 6     | 🛡️ Reliability   | Crash recovery, idempotency, human-in-the-loop                             | ⏳ Upcoming 01-Jan-2027 |
| 7     | 🔗 MCP / A2A  | MCP server + agent-agnostic evaluation                                           | ⏳ Upcoming 01-Feb-2027 |
| -     | ⏸️ Rest                                  | Buffer after Phase 2                                                                                                                     | ⏳ Upcoming 01-Mar-2027 |
| 8     | ⚡ Optimization     | Speculative decoding, quantization, caching                                            | ⏳ Upcoming 01-Apr-2027 |
| 9     | 🔒 Security       | Red-team suite + prompt injection defenses    | ⏳ Upcoming 01-May-2027 |
| 10    | 💸 Cost Routing    | Model routing cascade + cost attribution                 | ⏳ Upcoming 01-Jun-2027 |
| 11    | 🚀 Production     | CI/CD + SLOs + fine-tune decision                                             | ⏳ Upcoming 01-Jul-2027 |
| -     | ⏸️ Rest                                  | Buffer after Phase 3                                                                                                                     | ⏳ Upcoming 01-Aug-2027 |
| 12    | 🏗️ Platform        | Architecture consolidation                                  | ⏳ Upcoming 01-Sep-2027 |
| 13    | 📡 Observability   | Tracing, dashboards, drift detection                                  | ⏳ Upcoming 01-Oct-2027 |
| 14    | 🌍 Generalization | Second external agent evaluated end-to-end                          | ⏳ Upcoming 01-Nov-2027 |
| -     | ⏸️ Rest                                  | Buffer after Phase 4                                                                                                                     | ⏳ Upcoming 01-Dec-2027 |
| 15    | 🧩 SDK        | Plugin system + developer docs                                 | ⏳ Upcoming 01-Jan-2028 |
| 16    | ✍️ Leadership       | Design doc + tech radar + recorded talk                 | ⏳ Upcoming 01-Feb-2028 |
| 17    | 🌐 Portfolio           | Blog posts + open-source contributions                                 | ⏳ Upcoming 01-Mar-2028 |
| 18    | 🏁 Capstone  | Full integration + narrative + demo<                                    | ⏳ Upcoming 01-Apr-2028 |

---

## 🔗 Roadmap and Dependency Graph

Full roadmap details live in [`docs/ROADMAP.md`](./docs/ROADMAP.md). 

Read the graph notes and dependency table in [`docs/dependencies-graph.md`](./docs/dependencies-graph.md).

---

## 🎯 What the Finished Platform Should Do

If everything goes to plan, by Month 18 `banana` will be able to:

- Use both cloud AI APIs and local models through one shared interface
- Track cost and speed for every model call
- Measure quality with evals, test cases, and agent run results
- Run evals with rule-based checks, AI judge scoring, and automatic checks before code is merged
- Run a supervised coding agent that finds relevant code, suggests changes, asks for approval, and runs tests
- Check the agent’s steps, not just the final answer
- Recover if it crashes in the middle of a task
- Switch to a backup model if the main model fails
- Ask a human before doing risky things like editing files or running shell commands
- Protect against prompt injection, unsafe tool use, and leaked secrets
- Expose its core tools through MCP so compatible clients can connect
- Choose between local models and cloud APIs based on quality, cost, speed, and confidence
- Trace each agent run from start to finish, including cost and latency for each step
- Alert when quality starts getting worse over time
- Let people add new tools or agents through a plugin SDK, while getting evals, safety, and observability by default

Most importantly, `banana` will be tested on at least two agents: one I built, and one I did not build.

Generalization has to be proven, not assumed.

---

## 🧰 Tech Stack

| Layer | Tools |
|-------|-------|
| 🖥️ **Local inference** | Ollama, llama.cpp (any local machine) |
| ☁️ **Cloud APIs** | OpenAI, Anthropic, Google (via LiteLLM / OpenRouter) |
| 🤖 **Agent framework** | LangGraph |
| 🔗 **Protocols** | MCP (Model Context Protocol), A2A |
| 🧪 **Evaluation** | Custom harness (built Month 2) |
| 📡 **Observability** | OpenTelemetry + Langfuse (self-hosted) |
| 🐍 **Language** | Python |

---

## ⚙️ Repository Structure

```
banana18/
├── src/
│   └── banana/
│       ├── clients/         # Model clients and instrumentation
│       ├── evaluation/      # Eval harness, judges, viewers, gates
│       ├── agents/          # Supervised coding agent workflows
│       ├── trajectory/      # Trajectory scoring and failure taxonomy
│       ├── orchestration/   # Multi-agent workflow coordination
│       ├── reliability/     # Checkpointing, recovery, HITL
│       ├── protocols/       # MCP, A2A, agent interfaces
│       ├── optimization/    # Inference and runtime optimization
│       ├── security/        # Guardrails and red-team tooling
│       ├── routing/         # Cost-aware model routing
│       ├── production/      # CI/CD, SLOs, deployment support
│       ├── platform/        # Evaluation platform and SDK
│       └── observability/   # Tracing, dashboards, drift detection
├── tests/
├── docs/
│   ├── ROADMAP.md
│   ├── dependencies-graph.md
│   ├── months/              # Monthly write-ups
│   └── assets/
│       └── dependencies-graph.png
├── pyproject.toml
└── README.md
```

---


## 📚What Gets Published
At the start of each month, I will publish a lesson plan for that month. This will explain what I plan to study, build, and measure.

During the month, I will share my progress openly: what I built, what I learned, what resources I found, what results I got, and what I am thinking through. I will also ask for help when I get stuck and share updates in the Discord channel with everyone following along.

Each month, I will also write about:

- What I planned to build
- What I actually built
- The numbers: quality, cost, and latency
- What broke
- What the failure taught me
- What I would do differently next time

These updates will live in [`/docs/months`](./docs/months) and will also be cross-posted publicly.

The writing is part of the work, not a bonus on top of it.

## 🤝 Contributing

Contributions are welcome when they make the roadmap more practical, measurable, or useful to builders. Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before opening a large issue or pull request.


## 📝 A Note on Plans

This is a plan. Plans meet reality and get revised. Some tools in the stack will change. Some months will go slower than expected. Some things I think will be hard will turn out to be easy, and vice versa - that's almost certain.

What won't change: the one rule, the commitment to measuring everything, and the public documentation of what actually happened versus what I thought would happen.

The honest gap between plan and reality is usually where the most useful learning lives.

---

## 🤖 AI-Generated Content Note

Parts of this roadmap and documentation were generated or revised with AI assistance. Treat them as a working plan, not a guarantee. If something looks unrealistic, misleading, outdated, or poorly grounded in real engineering practice, please [open an issue](https://github.com/bttrung/banana18/issues) with the specific concern.

---

<div align="center">

### 💬 Following along or building something similar? [Join the Discord](https://discord.gg/ETFrkZCtp)

*Starting July 2026 · MIT License · Built in public*

</div>
