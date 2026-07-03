# Month 01 - The Instrumented AI Client
### Applied AI Engineer Roadmap · Instructor's Edition (Professor's Notes)

---

> **Teaching philosophy.** Here's the deal. Most people start their AI journey by `pip install`-ing a framework, calling `.run()`, getting a plausible-looking answer, and declaring victory. That's not engineering - that's gambling with someone else's chips. This month you build the one thing every later month stands on: a thin, boring, fully-instrumented client that talks to *any* model - your local Qwen on Ollama, a second local backend (MLX on Apple Silicon, or llama.cpp on an NVIDIA GPU / CPU), or a frontier API - through one interface, and **earns three numbers on every single call**. You are not building intelligence this month. You're building the *measuring instrument* you'll use to judge intelligence for the next 17 months.
>
> An AI call is just an HTTP request with a weird, expensive, non-deterministic payload - you already know how to wrap a flaky upstream service in retries, timeouts, and telemetry. We're going to do exactly that, and refuse to add a single line of "smart" behavior until the dumb, measured version works. This is the foundation of `banana`: the client that Month 2's eval harness will call, that Month 3's agent will call, that Month 10's router will sit on top of. Build it wrong and everything above it inherits the rot.
>
> **The one rule of this month:** *No call leaves my client without recording tokens, cost, latency, and memory. A call I can't measure is a call I don't trust.*

---

## Month 1 Learning Outcomes (what you must be able to DO by Day 30)

By the end of this month, without notes, you can:

1. **BUILD** - a single Python client interface (`generate()` / `stream()`) that drives three backends - Ollama (local), a second local backend of your choice (MLX on Apple Silicon, or llama.cpp on an NVIDIA GPU / CPU), and one cloud API (Anthropic or OpenAI) - where swapping backend changes *nothing* at the call site except a string.
2. **BUILD** - a telemetry layer that attaches `{tokens_in, tokens_out, tokens_per_sec, ttft_ms, total_ms, est_cost_usd, peak_ram_mb}` to *every* call and persists it to a queryable log (JSONL or SQLite).
3. **MEASURE** - time-to-first-token (TTFT), tokens/sec, and peak RAM for at least **two local model sizes** (e.g., Qwen2.5-Coder 7B and 14B) against a cloud baseline, and quote the numbers within ±5% across three runs.
4. **MEASURE** - how `temperature` and `top_p` move a real quality proxy - **structured-output parse-failure rate** - across at least four settings, reported as a curve with error bars, not a vibe.
5. **BREAK** - the client deliberately (model outage, context overflow, malformed JSON, an oversized model that swaps) and show your retry/timeout/parse-guard logic degrades gracefully instead of hanging or crashing.
6. **DEFEND** - the honest gap: state, with your own numbers, exactly where local loses to cloud (and where it wins), and the threshold that would make you route to an API.
7. **DEFEND** - from memory, the lifecycle of one completion call - from your function, to tokens, to TTFT, to the streamed bytes - and predict where it breaks under load.

> **Assessment is behavioral.** Each week ends with a pass/fail checkpoint. The month ends with a recorded ~10-minute oral defense where you run the client live, trigger a failure and show it recover, explain the call lifecycle from memory, and honestly state where local loses to cloud. If you can't do it on camera, you can't put it in your portfolio.

---

> **Choosing your two local backends (any hardware works).** The interface drives three backends, and the *second local* one is yours to pick by hardware - that's exactly why the interface stays portable:
> - **Apple Silicon:** Ollama + **MLX** (Apple-native, fast, runs in unified memory); read peak memory with `mlx.core.get_peak_memory()`.
> - **NVIDIA GPU / Windows / Linux:** Ollama + **llama.cpp** (both cross-platform, both expose an OpenAI-compatible server); read peak memory with `nvidia-smi` / `torch.cuda.max_memory_allocated()`.
> - **CPU-only / low-resource:** Ollama + **llama.cpp** with a small GGUF model; read peak memory with `psutil` RSS, and lean on the cloud backend for heavier tasks.
>
> Everything else - the unified interface, retries, timeouts, structured-output parsing, the telemetry layer, the temperature→parse-failure sweep - is identical on every platform. The whole point of the month is that *swapping a backend changes one string at the call site*; wherever this plan names MLX, the llama.cpp path is the cross-platform substitute (and llama.cpp runs on Apple too, so if you want a single portable stack, that's it).

## The Mental Model / "Spine"

Pin this. Everything in Month 1 hangs off it:

> **An LLM call is a flaky, metered, non-deterministic upstream service.** You wrap it the way you'd wrap any such service - one interface, retries, timeouts, structured-output parsing, and telemetry on every call - and you trust nothing you haven't measured. The client doesn't make the model *smart*; it makes the model *observable*. Everything you build for the next 17 months is observable only because this layer is.

**There is no prior month to connect to - this is the slab.** Month 1 is where the discipline starts: *a model call is a metered, stateless transaction.* Every later spine builds on this one.

**Connection forward:** Month 2's eval harness doesn't call OpenAI or Ollama - it calls *your* `client.complete()`, so every eval result inherits this telemetry for free. The parse-failure rate you measure in Week 4 is the *seed* of QUALITY; next month it grows into a full coding-task pass rate. The retry/timeout discipline you hand-roll is what keeps Month 6's agent from double-applying a file edit. The local-vs-cloud table is the embryo of Month 10's router. You are not doing throwaway work; you are pouring the foundation.

---

# WEEK 1 - "Make one call, and instrument it": the raw, measured request

**Theme:** One backend, raw, measured. No abstractions yet - you earn the right to abstract by first feeling the raw call. Before you wrap anything, you must see exactly what bytes go out and what comes back.

---

### Concept block (~2h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 1.1 (60m) | **Andrej Karpathy - "Intro to LLMs"** (video) | **Intuition ONLY.** Extract three things: (1) what a *token* is - not a word, a sub-word fragment; (2) what "next-token prediction" means and why the same input can yield different output; (3) why a context window is a hard, finite budget. Stop when you can explain each in one sentence. Do **not** go near attention math - if you open a transformer paper this week, you've failed the week. |
| 1.2 (30m) | **Ollama docs - API reference** (`/api/generate`, `/api/chat`, `stream`) | The exact request/response shape. Where `prompt_eval_count`, `eval_count`, `eval_duration`, and `prompt_eval_duration` live in the streamed response - **that is your token-count and timing data, for free.** How streaming chunks arrive (newline-delimited JSON) and which chunk carries the final stats. |
| 1.3 (30m) | **Chip Huyen - *AI Engineering*, ch. 1–2** (skim) | The working vocabulary: context window, tokens, temperature, top_p, sampling. One purpose only: map each term to an API parameter you will actually send in a payload this week. Skim - you return to this book all year. |

> **Professor's Note - earn the abstraction.** Your instinct as an experienced engineer is to design the interface first: define `LLMClient`, sketch the backends, make it clean. Resist for exactly one week. You cannot design a good wrapper around a thing you've never touched raw. Make the ugly `httpx` POST yourself. Parse the stream by hand. *Feel* where the first token arrives. Then - and only then - do you know what the abstraction must hide and what it must expose. This is the same reason you read a raw SQL query log before trusting an ORM. The wrapper that hides something you never saw is the wrapper that lies to you in production.

---

### Lab 1 - BUILD: the rawest possible call, no SDK, no framework (~2.5h)

**Goal:** A standalone script that POSTs to Ollama directly, parses the streamed response by hand, and prints five numbers. No `ollama` Python package, no LangChain, no LiteLLM. Just `httpx` and your own parsing.

**Steps:**

1. **Pull a model and confirm it's loaded:**
   ```bash
   ollama pull qwen2.5-coder:7b
   ollama ps                      # confirm it's resident, note the size
   ollama show qwen2.5-coder:7b   # note the context length - you need it in Lab 2
   ```

2. **Write `raw_call.py`** that streams a completion by hand:
   ```python
   import httpx, json, time

   def raw_generate(prompt: str, model: str = "qwen2.5-coder:7b"):
       url = "http://localhost:11434/api/generate"
       payload = {"model": model, "prompt": prompt, "stream": True}
       t_start = time.perf_counter()
       ttft = None
       final = {}
       with httpx.stream("POST", url, json=payload, timeout=120) as r:
           for line in r.iter_lines():
               if not line:
                   continue
               chunk = json.loads(line)
               if ttft is None and chunk.get("response"):
                   ttft = time.perf_counter() - t_start   # first token arrived
               if chunk.get("done"):
                   final = chunk                           # carries the stats
       total = time.perf_counter() - t_start
       return ttft, total, final
   ```

3. **Pull the real numbers from the final chunk.** Ollama reports `prompt_eval_count` (input tokens), `eval_count` (output tokens), and `eval_duration` (ns spent generating). Compute tokens/sec as `eval_count / (eval_duration / 1e9)`.

4. **Print all five numbers:** `prompt_tokens, completion_tokens, ttft_ms, total_ms, tokens_per_sec`.

5. **Run it three times on the same prompt** and eyeball the variance.

**ACCEPTANCE:** `python raw_call.py` prints all five numbers, parsed by hand from a stream you read yourself - zero SDK calls. You can point to the exact line where TTFT is captured and the exact field where output-token count comes from.

**Target number:** TTFT and tokens/sec for 7B, reproducible within **±5%** across 3 runs on the same prompt.

---

### Lab 2 - BREAK: overflow the context window (~1.5h)

**Goal:** Discover what your backend does when you exceed its context budget - *before* it silently corrupts a run in Month 3. Then build a guard.

**Steps:**

1. **Find the model's context length** from `ollama show qwen2.5-coder:7b` (the `context length` field).

2. **Deliberately exceed it.** Take a large source file and paste it into the prompt 10×, or generate a prompt you've estimated (chars ÷ 4 ≈ tokens) to be well over the limit. Send it through `raw_call.py`.

3. **Observe and record the behavior.** Does Ollama:
   - Silently truncate the front of the prompt (most dangerous - you lose context and never know)?
   - Return an error?
   - Stall or slow dramatically?
     Write down exactly what happened and at roughly what token count it changed.

4. **Build a pre-flight guard.** Add a rough token estimate (chars ÷ 4 is fine for now - you'll replace it with a real tokenizer in Week 3) and a check that *refuses or truncates before sending*, logging which action it took and why.

**ACCEPTANCE:** An oversized prompt can never silently corrupt a run. Your guard catches it, logs the reason, and either refuses or truncates deliberately. You have documented what Ollama does *without* the guard.

**Target number:** The approximate token count at which the backend's behavior changes - recorded as data.

> **Professor's Note - silent truncation is the bug you won't find for three months.** In a normal API, exceeding a limit gives you a `413` and you move on. Some LLM backends just drop the part of the prompt that doesn't fit - usually the *front*, where your system instructions live - and answer confidently from the mangled remainder. The output looks fine. It is not fine. This is the single most common source of "why did the agent suddenly ignore its instructions?" in Month 6. You're catching it now, cheaply, with a guard and a log line.

---

### Deep-Understanding Drill - Week 1

**From-memory exercise (~30m):** On paper - no IDE - **draw the full lifecycle of one streaming completion**:

```
your function → httpx POST → Ollama server → model load (if cold) →
  prompt tokenization → first generated token (TTFT measured HERE) →
  streamed chunks → your line parser → final "done" chunk (stats HERE) →
  your metrics
```

For each stage, answer:
1. What can go wrong here? (cold model, network, truncation, parse error)
2. Which number is measured at which point - and why is TTFT measured at the *first* token, not the request send?

Then predict: *if the model were twice as large (14B instead of 7B), which number degrades first - TTFT, tokens/sec, or peak RAM - and why?* Write your prediction down. You'll test it in Week 3.

**ACCEPTANCE:** A hand-drawn diagram with failure annotations and your degradation prediction, saved for the oral defense.

---

### ✅ Week 1 Checkpoint (pass/fail)

- [ ] Raw streamed call works **without** any SDK or framework - just `httpx` and hand parsing
- [ ] Five numbers printed per call: prompt tokens, completion tokens, TTFT, total, tokens/sec
- [ ] Context overflow behavior is documented, and a pre-flight guard catches oversized input
- [ ] You can quote 7B TTFT and tokens/sec within ±5% across 3 runs
- [ ] Lifecycle diagram drawn from memory with a degradation prediction

**Target number:** Your first reproducible latency numbers - e.g., "qwen2.5-coder:7b: TTFT ~280ms, ~38 tok/s on your machine, ±5% over 3 runs." Write it down. This is the baseline the rest of the month measures against.

---

### Socratic Questions - Week 1

1. Why is TTFT often a *better* UX metric than total latency for an interactive coding tool - and when does that flip? (Hint: think streaming chat vs. a one-shot "generate this whole file" call.)
2. Your tokens/sec changed between run 1 and run 2 on the *exact same prompt*. Name two mechanical reasons - one inside the model, one inside your machine. (Hint: one rhymes with "thermal," one with "cache.")
3. Ollama handed you `eval_count` for free. If a provider *didn't* report output token count, how would you count it yourself - and how wrong could a chars÷4 estimate be?

---

# WEEK 2 - "One interface, three backends": the unified client and the retry contract

**Theme:** Now that you've felt the raw call, abstract it - *deliberately*. One interface, three concrete backends, swap with a string. Plus the thing that separates a toy from a client: it survives a flaky upstream. This is where you learn that an LLM endpoint is a non-idempotent, rate-limited service, and you treat it like one.

---

### Concept block (~2h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 2.1 (30m) | **Your second local backend's README** - MLX / `mlx-lm` (Apple) *or* `llama.cpp` (cross-platform) | How to run a model two ways: one-shot generation and an OpenAI-compatible HTTP server (`mlx_lm.server`, or `llama-server`). The key fact you're after: how this backend uses memory and how to read peak memory - `mlx.core.get_peak_memory()` on MLX (unified memory, no separate VRAM copy), or `nvidia-smi` / `torch.cuda.max_memory_allocated()` with llama.cpp on a GPU. This is the fast local path for your hardware. |
| 2.2 (30m) | **Anthropic *or* OpenAI API docs** (pick one as your cloud baseline) | The request shape, the *streaming* response shape, and - critically - the error and rate-limit responses (`429`, `529`/`503`) and *where* token usage is reported. You're matching your local backend's shape to this so one interface fits both. |
| 2.3 (30m) | **Chip Huyen - *AI Engineering*, structured-output / function-calling section** (skim) | Why models fail to emit valid JSON even when asked, and the standard mitigations: schema-in-prompt, retry, and repair. You'll implement all three. |
| 2.4 (30m) | Your own Week 1 code | Re-read `raw_call.py` and ask: "What in here is Ollama-specific, and what is universal?" The universal part becomes the interface; the specific part becomes a backend. This is the design work. |

> **Professor's Note - the anchor: this is a flaky third-party integration.** You have wrapped a payment gateway, a shipping API, an SMS provider. You know the drill: timeout, retry with backoff, circuit-break, log every attempt. An LLM endpoint is exactly that - *with one vicious twist.* A `POST /charge` is idempotent if you send an idempotency key; the same key never double-charges. An LLM completion is **not idempotent** - the same prompt returns *different text* every time. So "retry" doesn't mean "re-run the same request"; it means "ask again and get a *different* answer." That single fact is why naive agent loops in Month 6 double-apply edits and burn money. Feel it now, cheaply, with a print statement.

---

### Lab 3 - BUILD: the unified client, hand-rolled before any framework (~3h)

**Goal:** One interface, three backends. Swapping providers changes a single string at the call site. You build this *by hand* so that when you later evaluate LiteLLM or LangChain, you know exactly what they hide.

**Steps:**

1. **Define the directory structure** inside `banana`:
   ```
   banana/
   ├── client/
   │   ├── __init__.py
   │   ├── client.py          # The LLMClient interface
   │   ├── backends/
   │   │   ├── ollama.py      # OllamaBackend
   │   │   ├── local2.py      # second local backend: MLX (Apple) or llama.cpp (GPU/CPU), via its OpenAI-compatible server
   │   │   └── cloud.py       # CloudBackend (Anthropic or OpenAI)
   │   ├── telemetry.py       # (Week 3)
   │   └── types.py           # CompletionResponse, Result dataclasses
   ```

2. **Define the one interface and the one return type:**
   ```python
   @dataclass
   class CompletionResponse:
       text: str
       backend: str
       model: str
       # telemetry (fully populated in Week 3)
       prompt_tokens: int
       completion_tokens: int
       tokens_per_sec: float
       ttft_ms: float
       total_ms: float
       est_cost_usd: float
       peak_ram_mb: float
       # structured-output result
       parse_ok: bool
       parsed: Optional[dict]

   class LLMClient:
       def __init__(self, backend: str): ...
       def generate(self, prompt: str, *, schema=None, **sampling) -> CompletionResponse: ...
       def stream(self, prompt: str, **sampling): ...   # yields chunks
   ```

3. **Implement three backends behind the interface:**
   - `OllamaBackend` - refactor your Week 1 `raw_call.py` into this.
   - Second local backend - run its OpenAI-compatible server on `localhost:8080` and talk to it over HTTP: `mlx_lm.server` on Apple, or `llama-server` (llama.cpp) on a GPU/CPU.
   - `CloudBackend` - Anthropic or OpenAI SDK; map their usage fields into `CompletionResponse`.

4. **The only call-site change is the backend string:**
   ```python
   for backend in ("ollama", "local2", "cloud"):   # "local2" = "mlx" on Apple, "llamacpp" on GPU/CPU
       r = LLMClient(backend).generate("Fix the off-by-one bug in this loop: ...")
       print(backend, r.completion_tokens, r.ttft_ms)
   ```

5. **Add structured-output parsing.** When `schema` is passed, parse the response as JSON, validate against the schema, and set `parse_ok: bool` + `parsed`. Do **not** throw on failure - record it.

**ACCEPTANCE:** `LLMClient("ollama").generate(p)`, `LLMClient("local2").generate(p)` (your MLX or llama.cpp backend), and `LLMClient("cloud").generate(p)` all return a `CompletionResponse` with **identical shape**. The same prompt through three backends produces three comparable telemetry rows side by side.

**Target number:** One prompt → three backends → three telemetry rows, displayed together.

> **Constraint check - mechanism before framework.** Do NOT reach for LiteLLM or LangChain here. The whole point is that you will *understand what they hide* because you wrote the dumb version first. You may adopt LiteLLM as late as Month 10 - but only once you can state, line by line, what it's doing for you. Convenience you can't explain is risk you can't debug.

---

### Lab 4 - BREAK: outage + malformed JSON, then make it survive (~2h)

**Goal:** Inject the two failures every LLM client hits in production - a flaky/rate-limited upstream and an unparseable response - and make your client degrade gracefully instead of hanging or throwing raw.

**Steps:**

1. **Simulate a cloud outage.** Point the cloud backend at a dead port, or wrap it to raise `429`/`503` on the first two attempts, then succeed. This mimics a real rate-limit burst.

2. **Add retry with exponential backoff + jitter and a hard per-call timeout.** Cap retries (e.g., 3). Log every attempt with its delay:
   ```python
   delay = base * (2 ** attempt) + random.uniform(0, jitter)
   ```
   On the final failure, return a *structured* error in `CompletionResponse` - never let a raw exception escape to the caller.

3. **Force a parse failure.** Ask for strict JSON at `temperature=1.5` until the model emits trailing prose (`{...}  Hope that helps!`). Add a single **repair attempt** (re-prompt: "Return ONLY valid JSON, no prose"), then fail cleanly with `parse_ok=False` if it still fails.

4. **Run a 20-call fault-injection batch** mixing outages and parse failures. Count unhandled exceptions (target: zero) and confirm every call returns a structured result.

**ACCEPTANCE:** The injected outage recovers within the retry budget; an unrecoverable call returns a structured error and never hangs or throws raw. A 20-call fault-injection run produces **zero** unhandled exceptions.

**Target number:** Recovery within ≤3 attempts; **0** unhandled exceptions across the 20-call fault run.

> **Professor's Note - the judgment this week teaches.** A retry on a `GET` is free. A retry on an LLM completion is *not the same request* - it's a fresh, differently-priced, differently-worded answer. So you must ask, every time: *is this operation safe to retry?* For a read-only "summarize this," yes. For "apply this patch to my repo" (Month 6), retrying blindly can apply the edit twice. The discipline you build now - log every attempt, cap the budget, classify what's safe to repeat - is what stands between you and a corrupted working tree later.

---

### Deep-Understanding Drill - Week 2

**From-scratch exercise (~45m):** Implement **retry-with-exponential-backoff-and-jitter** yourself in < 30 lines - no `tenacity`, no `backoff` library. Then answer in writing (½ page):

> *Is an LLM completion call idempotent?* Compare it to a `POST /payments` with an idempotency key. What does "retry" even mean when the same prompt returns different text each time? What would you have to add to make retries **safe** for a tool that writes files (foreshadowing Month 6)?

**Why:** The retry loop is the abstraction every HTTP library hides from you. If you can't write it in 30 lines, you don't actually understand what `tenacity` does - and you can't reason about whether a retry is safe for a *side-effecting* call. The idempotency question is the one that bites hardest in Month 6, and you want to have already thought it through.

**ACCEPTANCE:** A standalone < 30-line backoff function plus a written half-page on LLM-call idempotency. Saved for the oral defense.

---

### ✅ Week 2 Checkpoint (pass/fail)

- [ ] One interface, three backends (Ollama, your second local backend, cloud), swapped with a single string
- [ ] `CompletionResponse` has identical shape across all three backends
- [ ] Retry + timeout + backoff implemented **by hand** and verified with injected faults
- [ ] Structured-output parsing with a `parse_ok` flag that never throws
- [ ] Zero unhandled exceptions across a 20-call fault-injection run
- [ ] Minimal hand-rolled backoff (< 30 lines) works independently

**Target numbers:** Recovery within ≤3 attempts; 0 unhandled exceptions in the fault run.

---

### Socratic Questions - Week 2

1. Your cloud backend and your Ollama backend report token usage in *different fields with different tokenizers*. Where exactly does that asymmetry bite you when you try to compare cost fairly in Week 3?
2. You added a JSON-repair retry. What's the hidden cost of that retry (think latency *and* tokens), and how would you decide it's not worth it for a given task?
3. Why might your local backend show *lower* peak memory than you'd predict from the model file's size on disk? (Hint: quantization - and, on Apple's unified memory, there's no second copy in a separate VRAM pool.)

---

# WEEK 3 - "Every call earns three numbers": the telemetry and cost layer

**Theme:** Telemetry stops being a print statement and becomes infrastructure. Every call lands in a queryable log with all the numbers. You learn that "cost" means *two different things* this year, and you build a meter you can actually trust - by deliberately breaking it first.

---

### Concept block (~1.5h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 3.1 (30m) | **`tiktoken` docs** + your provider's tokenizer notes | How to count tokens *before* you send (for cost estimation), and why local and cloud tokenizers disagree on the same string. The token count is the unit of cost - get it wrong and your whole cost model is wrong. |
| 3.2 (30m) | **Anthropic / OpenAI pricing page** | The exact $/1M *input* and $/1M *output* tokens for your baseline model. Note that input and output are priced differently - this matters for the cost formula. Cloud cost is real money; local cost is energy + time. |
| 3.3 (30m) | **Your platform's power + memory tools** - macOS `powermetrics` + `mlx.core.get_peak_memory()` (Apple); `nvidia-smi` + `torch.cuda.max_memory_allocated()` (NVIDIA GPU); `psutil` RSS + your OS power readout (CPU/Linux) | How to read watts and peak memory use *on your actual machine*. You can't quote a local cost number you didn't measure on your own hardware. |

> **Professor's Note - COST means two things this year, and merging them is the first lie that compounds.** For **local**, cost = "can it run at acceptable latency on-device?" There is no per-token bill - the marginal cost of one more call is ≈ $0, but you pay in latency ceiling and RAM. For **cloud**, cost = "dollars vs. the hosted baseline" - real money, scales linearly with tokens, but no latency ceiling you control. When you write the comparison, keep them as **two columns**, never one merged dollar figure. The day you mush them together is the day your Month 10 routing decision is built on a number that means nothing. The honesty *is* the engineering.

---

### Lab 5 - BUILD: the telemetry + cost layer (~3h)

**Goal:** Every call, through any backend, lands in a queryable log with all eight numbers. Cost is estimated for cloud and *measured* for local.

**Steps:**

1. **Wrap every backend call** so it emits one record per call to `logs/calls.jsonl` (or a SQLite table):
   ```json
   {"ts": "...", "backend": "ollama", "model": "qwen2.5-coder:7b",
    "prompt_tokens": 412, "completion_tokens": 156, "tokens_per_sec": 37.8,
    "ttft_ms": 281, "total_ms": 4130, "peak_ram_mb": 8214, "est_cost_usd": 0.0}
   ```

2. **Cloud cost** - use the real pricing, input and output priced separately:
   ```python
   est_cost_usd = (in_tokens / 1e6) * price_in + (out_tokens / 1e6) * price_out
   ```

3. **Local cost** - measure, don't guess. Sample average watts during a generation, using whichever tool fits your hardware:
   ```bash
   # Apple Silicon (macOS):
   sudo powermetrics --samplers cpu_power,gpu_power -n 1 -i 1000
   # NVIDIA GPU:
   nvidia-smi --query-gpu=power.draw --format=csv -l 1
   # CPU-only / Linux without a discrete GPU: read your OS power sensor
   # (e.g. `turbostat`, RAPL via `powercap`, or estimate from TDP)
   ```
   Multiply average watts × wall-time × your local $/kWh to get an *energy* cost. Record energy cost and the *time* cost as **separate** fields - they are different quantities.

4. **Memory** - capture peak memory the way your backend exposes it: process RSS via `psutil` (any platform), `mlx.core.get_peak_memory()` (Apple/MLX), `torch.cuda.max_memory_allocated()` or `nvidia-smi` (NVIDIA GPU), and Ollama's reported size from `ollama ps`.

5. **Add a query helper** - a tiny function or `make` target that reads `calls.jsonl` and prints a per-backend summary table (median TTFT, median tok/s, total cost, peak RAM).

**ACCEPTANCE:** 100% of calls in a 30-call run land in the log with all eight fields populated. You can query the log and produce a per-backend summary table.

**Target number:** Your cloud cost estimate is within **±10%** of the provider's own usage dashboard for the same run.

---

### Lab 6 - BREAK: trust-but-verify your own meter (~2h)

**Goal:** A meter you haven't verified is a meter that lies. Deliberately break your token counting and your memory assumptions, quantify how wrong they are, then fix them.

**Steps:**

1. **Break the token count.** Replace your real token counting with the naive chars ÷ 4 estimate. Run a 20-call batch through the cloud backend. Compare your `est_cost_usd` total to the provider's dashboard. **Quantify the error** (e.g., "chars÷4 overestimated cost by 18%").

2. **Fix it** with `tiktoken` (cloud) and the backend's actual reported token counts (local). Re-run the same batch. Re-compare. Record the before/after accuracy.

3. **Break the memory story.** Load a model too big for your memory budget - e.g., a 32B (Q4) on a 16 GB machine - and watch it degrade. On Apple/CPU it spills to SSD-swap; on an NVIDIA GPU it errors out or forces CPU-offload. Capture the tokens/sec collapse and peak memory as it hits the wall. **This is the moment you confirm or refute your Week 1 prediction** about which number degrades first.

4. **Document the swap-point** - the model size / context combination where "bigger model" became "worse experience," with the exact tokens/sec drop.

**ACCEPTANCE:** You have a before/after on cost-estimate accuracy (chars÷4 vs. real tokenizer) and a documented swap-point with the tokens/sec collapse quantified.

**Target number:** The tokens/sec drop at the swap-point, quantified - e.g., "7B fits: 38 tok/s → 32B swapping: 3 tok/s, peak RAM 15.8/16 GB."

> **Professor's Note - this is mutation testing for your meter.** You verified your retry logic by injecting outages. Now you verify your *measurement* by injecting a known-wrong tokenizer and seeing how far off the cost goes. A cost model you never checked against the provider's dashboard is a guess wearing a lab coat. The 18% error you just measured? Imagine it silently compounding across 100k calls/day in Month 11. You found it now, for free, with a deliberate bug.

---

### Deep-Understanding Drill - Week 3

**From-scratch exercise (~45m):** Write a < 30-line `estimate_cost(prompt, model)` that token-counts and prices a call **before** sending it. Then explain, in writing (½ page):

> Why are TTFT and total latency *different numbers*? Why does tokens/sec alone fail to predict user-perceived speed? And why is your local "cost" a fundamentally different *quantity* than cloud cost - not just a smaller number?

**Why:** If you can predict cost before sending, you can build a router (Month 10). If you can't articulate why local and cloud cost are different *kinds* of things, you'll write a dishonest comparison table - and a reviewer will shred it. This drill is the thinking behind the "two columns, never merged" rule.

**ACCEPTANCE:** A standalone `estimate_cost` function plus the written half-page. Saved for the oral defense.

---

### ✅ Week 3 Checkpoint (pass/fail)

- [ ] 100% of calls logged to `calls.jsonl` (or SQLite) with all eight fields
- [ ] Cloud cost estimate within ±10% of the provider's real dashboard
- [ ] Local energy cost **and** time cost recorded as separate fields (not merged)
- [ ] Swap-point documented with the tokens/sec collapse
- [ ] Week 1's degradation prediction confirmed or refuted with data
- [ ] `estimate_cost` (< 30 lines) works independently

**Target numbers:** Cost-estimate accuracy before/after the tokenizer fix; the swap-point tokens/sec drop.

---

### Socratic Questions - Week 3

1. Your `est_cost_usd` was off by 18% before you fixed the tokenizer. In a system making 100k calls/day, what does an 18% accounting error cost you in *trust*, not just dollars - and who notices first?
2. Peak memory hit 15.6 GB on your 16 GB machine and tokens/sec cratered. Explain the *mechanism* - what is your OS actually doing (SSD-swap on Apple/CPU, or OOM / CPU-offload on a GPU), and why is a *smaller* model that fits often the right call even if it's "less capable"?
3. If you could log only ONE number per call for the rest of the year, which would it be and why? (There's no single right answer - defend yours.)

---

# WEEK 4 - "Measure the tradeoff, publish the gap": the sampling sweep and the honest comparison

**Theme:** Turn the instrument on the question that matters. Measure how sampling settings move quality, find where local genuinely loses to cloud, and publish it honestly. This week produces the parse-failure curve that *seeds the Month 2 eval harness* and your first calibrated-honesty artifact.

---

### Concept block (~1h)

| Session | Source | What to EXTRACT |
|---|---|---|
| 4.1 (15m) | **Provider docs on `temperature` / `top_p`** | The precise definition of each knob and the standard advice: tune one at a time, not both. Temperature reshapes the whole distribution; top_p truncates its tail. |
| 4.2 (30m) | **Chip Huyen - *AI Engineering*, sampling section** | Why higher temperature raises output *diversity* **and** malformed-output rate simultaneously - that's the exact tradeoff you're about to put a number on. |
| 4.3 (15m) | **Barbara Minto - *The Pyramid Principle*** (skim) | Conclusion-first writing. You'll use it on the write-up: lead with the recommendation, *then* the numbers, *then* the method. A reviewer should get your answer in the first sentence. |

> **Professor's Note - parse-failure rate is the seed of the entire eval harness.** It feels crude: "did the JSON parse, yes or no?" That crudeness is exactly *why* it's the right first quality metric - it's deterministic, free, and unambiguous. Next month you generalize it into the Month 2 eval harness (deterministic checks + a calibrated AI-as-judge). The discipline you set *now* - fixed prompt set, multiple trials, error bars, never a bare number - is the discipline you'll defend for 17 months. "87%" alone is a lie when n=20. "87% ± 9% (n=20)" is honest engineering. Build the habit this week, when the stakes are low.

---

### Lab 7 - MEASURE: the sampling sweep (the QUALITY seed) (~3h)

**Goal:** A reproducible experiment showing how `temperature` moves your structured-output parse-failure rate, plotted as a curve with error bars, across local and cloud.

**Steps:**

1. **Pick one structured task** and freeze a prompt set. Example: "Given this buggy function, return JSON `{\"bug\": str, \"fixed_code\": str}`." Build a fixed set of ~20 prompts (reuse small bugs - you'll formalize these into the Month 2 golden dataset).

2. **Sweep temperature** ∈ {0.0, 0.3, 0.7, 1.0, 1.5}, holding `top_p` fixed. For each setting, run all 20 prompts × 3 trials = 60 calls per setting, per backend.

3. **Record parse-failure rate** (your QUALITY proxy) and tokens/sec at each setting. Persist everything to your telemetry log from Week 3 - this experiment is just structured calls through your client.

4. **Plot parse-failure rate vs. temperature** for at least local 7B and the cloud baseline. Annotate with sample sizes.

5. **Report with error bars, never a bare number:** "parse-fail 6% ± 4% at temp 0.7 (n=60)."

**ACCEPTANCE:** A parse-failure-rate curve across ≥4 temperatures, for at least local 7B and the cloud baseline, with sample sizes and error bars. The whole sweep is reproducible via a committed script (`experiments/sampling_sweep.py`).

**Target number:** The temperature at which parse-failure rate crosses ~10%, per backend - the practical "diversity ceiling" for structured output.

---

### Lab 8 - BREAK + DEFEND: find where local loses, on purpose (~2h)

**Goal:** Deliberately construct the cases where local 7B fails and cloud succeeds. Quantify the gap. This is your first **calibrated-honesty** artifact - the single most credible thing in your portfolio.

**Steps:**

1. **Construct 3–5 hard prompts** you suspect local 7B will fail and cloud will nail - e.g., a subtle multi-function reasoning bug, a tricky edge case, a refactor that requires holding several constraints at once.

2. **Run both backends** on the hard set. Quantify the gap on two axes:
   - Parse-failure rate (automatic, from your client).
   - Eyeball correctness - *you*, the human, label each output pass/fail. This honest manual check is the embryo of Month 2's human labeling.

3. **Also record where local *wins*** - marginal cost ≈ $0, no rate limits, full privacy, no network dependency. Calibrated honesty cuts both ways.

4. **Write the routing rule the data implies:** "Below complexity X, local 7B at temp 0.3 is good enough and ~$0; above it, route to cloud - here's the measured gap." This rule is the embryo of Month 10's router.

**ACCEPTANCE:** A documented, numbered case where local genuinely loses, with the measured gap (quality + latency + cost) and the threshold that would make you route to an API. Plus at least one documented case where local *wins*.

**Target number:** The measured quality / latency / cost gap between local 7B and cloud on the hard set.

> **Professor's Note - "here's where it breaks" is the most valuable sentence in your portfolio.** The roadmap is deliberately local-first as a learning and cost vehicle - but most production AI is cloud-first, and pretending otherwise makes you look naive in an interview. The engineer who says "local 7B nails 80% of my coding tasks at ~$0, and here's the measured 20% where I route to cloud, with the threshold" is *more* credible than the one who claims local does everything. Hype is cheap. A measured gap with a routing threshold is the thing senior reviewers actually trust.

---

### Deep-Understanding Drill - Week 4

**Explain-it exercise (~30m):** Record a 2-minute voice memo (practice for the defense) explaining **temperature and top_p to a skeptical senior engineer** who says "just set temperature to zero and move on."

Cover:
1. What each knob does *mechanically* (temperature reshapes the distribution; top_p truncates the tail).
2. Why temp 0 isn't always best (it's deterministic-ish but can be repetitive and brittle on some tasks).
3. Why you measured parse-failure rate across a sweep instead of trusting your gut - and quote your actual crossover number.

**Why:** This is a conversation you'll have in every AI engineering job. If you can't justify a sampling choice with a number in two minutes, you'll lose the argument to whoever sounds most confident. The ability to defend the number is as important as producing it.

**ACCEPTANCE:** You recorded it. You quoted your actual crossover temperature and your parse-failure numbers with error bars.

---

### ✅ Week 4 Checkpoint (pass/fail)

- [ ] Parse-failure-rate vs. temperature curve, ≥4 settings, with error bars and n
- [ ] Sweep is reproducible via a committed script
- [ ] At least one documented case where local loses, with a routing threshold and measured gap
- [ ] At least one documented case where local wins
- [ ] The 1-page write-up drafted (see deliverables)
- [ ] You can defend every number's provenance from memory

**Target numbers:** The crossover temperature (~10% parse-fail) per backend; the measured local-vs-cloud gap on the hard set.

---

### Socratic Questions - Week 4

1. Parse-failure rate spiked from 5% to 40% between temp 1.0 and 1.5 on local, but only to 15% on cloud. What does that asymmetry tell you about the two models - and about how much you can trust a *small* model's structured output?
2. You found local "loses" on the hard set. Is that a *model* problem, a *prompt* problem, or a *sampling* problem - and how would you *prove* which one? (Hint: you have three knobs; change one at a time.)
3. If your boss said "just use the cloud API for everything, it's only money," what's your numbers-backed counter - and when would you actually *agree* with them?

---

# End-of-Month Deliverables

---

## Flagship Deliverable: The `banana` Instrumented AI Client (v0.1)

An increment of `banana` - the foundation, not a toy - that adds:

- **One client interface** (`banana/client/client.py`): `generate()` / `stream()` over **Ollama + a second local backend (MLX on Apple, or llama.cpp on GPU/CPU) + one cloud API**, swap by a single string at the call site
- **Three backends** (`banana/client/backends/`): each maps its provider's quirks into one `CompletionResponse` shape
- **Resilience**: retry with exponential backoff + jitter, hard per-call timeout, structured-output parsing with a `parse_ok` flag that never throws
- **Telemetry layer** (`banana/client/telemetry.py`): every call logs `{tokens_in, tokens_out, tokens_per_sec, ttft_ms, total_ms, est_cost_usd, peak_ram_mb}` to `logs/calls.jsonl`
- **Cost model**: cloud cost estimated from real pricing (verified within ±10% of the dashboard); local cost *measured* as separate energy and time columns
- **Sampling experiment** (`banana/experiments/sampling_sweep.py`): reproducible temperature sweep producing the parse-failure curve
- **Calibrated-honesty artifact**: a documented case where local loses to cloud, with a routing threshold

### The Three Numbers

| Metric | What it measures | Your number |
|---|---|---|
| **LATENCY** | TTFT + tokens/sec for ≥2 local model sizes (e.g., 7B and 14B) vs. cloud baseline | _Fill from your Week 1/3 runs_ |
| **QUALITY** | Structured-output parse-failure rate across the temperature sweep, with error bars and n | _Fill from your Week 4 sweep_ |
| **COST** | Local (energy + time, two columns) vs. cloud ($/call), with the routing threshold | _Fill from your Week 3 cost layer_ |

### The Repo

- All client code wired into `banana` (not a separate project)
- `logs/calls.jsonl` gitignored, but a sample summary table committed in the README
- `experiments/sampling_sweep.py` committed and reproducible
- README with the **three numbers**, a side-by-side local-vs-cloud table, and a "run it yourself" section
- `Makefile` targets: `make call` (one instrumented call), `make sweep` (run the sampling experiment), `make summary` (per-backend telemetry summary)
- Tagged `v0.1.0`
- **Public on GitHub** - this is the first `banana` increment

---

## Portfolio Artifact: The Blog Post

**Title:** *"Local vs Cloud AI - when to use which, with numbers from my machine."*

**Structure (Pyramid-style - conclusion first):**
1. **The recommendation, up front:** "For structured coding tasks under complexity X, local 7B at temp 0.3 is ~$0 and good enough; above X, route to cloud. Here's the data."
2. **The setup:** one client, three backends, every call measured. Why you built it by hand.
3. **The numbers:** the latency table (TTFT + tok/s, local sizes vs. cloud), the parse-failure curve, the two-column cost comparison.
4. **The honest gap:** the case where local loses, with the measured gap and the routing threshold. *And* where local wins (cost ≈ $0, privacy, no rate limits).
5. **What's next:** these crude parse-failure numbers become a real eval harness next month (Month 2 preview).

**Requirements:**
- Real numbers from *your* machine - latency, parse-failure rate with error bars, cost comparison
- At least one chart (the parse-failure-vs-temperature curve)
- At least one sentence acknowledging where your measurement is weak (e.g., "n=20 per setting gives wide error bars; I'd want n=100 for stable estimates")
- ≤ 1,500 words
- Published

---

## Oral Defense (~10 minutes, recorded)

Record a screen+voice walkthrough. You must demonstrate LIVE:

1. **Explain the call lifecycle from memory** (~2 min): Draw or show the lifecycle of one streaming completion - your function → POST → model → first token (TTFT) → streamed chunks → parser → metrics. Mark *exactly* where TTFT and tokens/sec are measured. Name what can go wrong at each stage. No reading off the screen.

2. **Live demo: one prompt, three backends** (~2 min): Run the same prompt through Ollama, your second local backend, and cloud. Show the three telemetry rows side by side. Point to the differences in TTFT, tokens/sec, and cost.

3. **Show a number and defend how you got it** (~3 min): Run the sampling sweep (or show committed results). Explain why you used error bars and a fixed prompt set, why parse-failure rate is a legitimate QUALITY proxy this early, and what your crossover temperature means. Then show your cost number and explain why local and cloud cost are *different quantities* (two columns, not merged) - and how you verified the cloud estimate against the dashboard.

4. **Break it live** (~2 min): Inject a model outage (dead port or forced 429). Show the retry recover within budget, and show the structured error on an unrecoverable failure. Then force a JSON parse failure and show `parse_ok=False` instead of a crash.

5. **The honest gap** (~1 min): Show the case where local loses to cloud, quote the measured gap, state your routing threshold - and say plainly where local *wins*.

---

## Month 1 Final Checkpoint (maps to the roadmap's "done")

- [ ] One interface → 3 backends (cloud, Ollama, a second local backend), swap with a string - *roadmap "done" #1*
- [ ] Every call auto-logs tokens, cost, TTFT + total latency, and memory - *roadmap "done" #2*
- [ ] Temperature/top_p experiment with real parse-failure numbers and error bars - *roadmap "done" #3*
- [ ] All three numbers captured for ≥2 model sizes, local vs. cloud
- [ ] Retry/timeout/backoff and structured-output parsing survive a fault-injection run with 0 unhandled exceptions
- [ ] Cloud cost estimate verified within ±10% of the provider dashboard
- [ ] Documented case where local loses, with a routing threshold
- [ ] Blog post published; repo public with README + numbers; tagged `v0.1.0`
- [ ] Oral defense recorded

---

# Common Mistakes for Month 1 - Expanded

---

### 1. Falling into the transformer-math rabbit hole

**What tempts you:** You watch Karpathy, get curious about attention heads, and three weeks later you have beautiful notes on QKV matrices and *zero* working code. The dopamine of "understanding" feels exactly like progress. It isn't.

**What to do instead:** Cap at intuition - token in, token out, non-deterministic, metered. Watch the video **once**. The moment you catch yourself opening a transformer paper this month, close it and go instrument another backend. You are *hiring* models, not designing them. The math is a different career; you can visit it later, once you have a shipped number.

**The test:** Is there working, measured code in your repo this week? If your notes are growing faster than your `logs/calls.jsonl`, you're in the rabbit hole.

---

### 2. Rebuilding LangChain from scratch

**What tempts you:** "I'll just make it a *little* general." Suddenly you have an abstract `BaseProvider` factory with plugin discovery, a config DSL, and a registry - and you still haven't made a single measured call.

**What to do instead:** Build the *thin* layer and nothing more: one interface, three concrete backends, retry, telemetry. Generality you didn't measure a need for is just unmeasured risk and a maintenance burden. The interface should be small enough to hold in your head.

**The test:** Count the abstractions in `client/`. If you have more base classes and factories than you have working backends, you've over-built. Three backends need three backend files, not a framework.

---

### 3. Blindly adopting a framework

**What tempts you:** Day 1, you `pip install langchain`, call `.invoke()`, get an answer - and now you have *no idea* what headers were sent, what retry happened, or what the call cost. It works, so you move on, blind.

**What to do instead:** Hand-roll the client first (Labs 1 and 3). You may adopt LiteLLM as late as Month 10 - but only once you can state, line by line, what it hides. The understanding is the deliverable; the wrapper is incidental. A framework you can't debug is a liability with good marketing.

**The test:** Can you explain what bytes left your machine on the last call, and what it cost? If a framework is answering that question for you and you can't verify it, you adopted too early.

---

### 4. Not measuring from day one

**What tempts you:** "I'll add telemetry once it works." It works. You move on. Now Month 8's optimization has no baseline to prove anything against, and Month 13's dashboard has nothing to read.

**What to do instead:** Telemetry goes in the *first* call (Lab 1), not bolted on later. The one rule of this month: no call leaves the client unmeasured. A baseline you didn't capture is gone forever - you cannot retroactively measure last week's latency.

**The test:** Open `logs/calls.jsonl`. Is there a record for *every* call you've made this month, or only the ones you remembered to instrument? Gaps in the log are gaps in your evidence.

---

### 5. Running a model too large for your memory budget

**What tempts you:** You download a 32B because bigger = smarter, then wonder why everything crawls (or the GPU just OOMs). You assume you did something wrong.

**What to do instead:** Match the model to the hardware: 7B–14B on 16 GB, up to 32B (Q4) on 32 GB+ (unified RAM on Apple, VRAM on a GPU, system RAM on CPU). Lab 6 makes you *feel* the wall - SSD-swap on Apple/CPU, OOM or CPU-offload on a GPU - so you never have to guess again. A 7B that fits beats a 32B that thrashes, and now you have the tokens/sec numbers to prove it in a code review.

**The test:** What's your machine's wall, in model size and tokens/sec? If you can't state it, you haven't run Lab 6 - and you'll keep mysteriously losing afternoons to a model that's thrashing your disk or refusing to load.

---

### 6. (ADDITIONAL) Comparing cloud and local on one merged "cost" number

**What tempts you:** A single dollar figure is tidy and fits in a slide. "Local is cheaper" - one number, done.

**What to do instead:** Local and cloud cost are *different physical quantities* - energy + latency-ceiling vs. dollars + throughput-ceiling. Keep them as two columns, always. Merging them produces a number that means nothing, and it's the first lie that compounds into a bad routing decision in Month 10.

**The test:** Does your cost comparison have two columns or one? If one, you've hidden the thing that actually drives the routing decision.

---

### 7. (ADDITIONAL) Trusting `eval_count` / usage fields without spot-checking

**What tempts you:** The API hands you token counts. Why wouldn't you trust them? They're right there in the response.

**What to do instead:** You broke and re-verified your meter in Lab 6 for a reason. Tokenizers disagree across providers, and a blind trust here makes your cost model quietly wrong by 10–20%. Trust, but verify against the provider dashboard at least once per provider.

**The test:** Have you reconciled your `est_cost_usd` total against the provider's billing dashboard for a real run? If not, your cost number is a guess wearing a lab coat.

---

# Weekly Rhythm Table

A realistic Mon–Sun schedule for someone with a full-time job (~10h/week).

| Day | Time | Activity | Type |
|---|---|---|---|
| **Mon** | 1h | Concept block: read *for* the week's purpose (the table says what to extract) | Read |
| **Tue** | 2h | Lab (primary): the week's main BUILD lab | Build |
| **Wed** | 1h | Finish concept reading + plan the BREAK lab | Read |
| **Thu** | 2h | Lab (secondary): MEASURE or BREAK lab | Build |
| **Fri** | 1h | Deep-Understanding Drill (from memory / from scratch) | Build |
| **Sat** | 2h | Finish labs, fill telemetry gaps, run the sweep | Build |
| **Sun** | 1h | Checkpoint + Socratic questions + reflection journal + commit/push + blog progress | Write |

**Totals:** ~2h read · ~6h build · ~2h write = **~10h/week**

> **The iron rule:** If a week is short, **cut the reading first. Never cut the build or the measurement.** A week where you read nothing but built the telemetry layer and captured real numbers is a successful week. A week where you watched three hours of LLM videos but never made a measured call is a wasted one. The Karpathy video and the Ollama API reference are the only near-mandatory reads this month - everything else can wait. The instrumented call cannot.

---

# Reflection Journal Prompts

Answer these after each week. Write 5–10 sentences, not paragraphs.

### Every week:
1. **What did I build, and does it work?** (Name the specific artifact and what "works" means - proven how?)
2. **What surprised me?** (Surprise = a gap in my mental model just closed. Name it.)
3. **Which Socratic question could I *not* answer cleanly?** (That's next week's real homework.)
4. **One thing I can now explain to a non-engineer that I couldn't before.**
5. **Which number do I trust *least* right now, and what would make me trust it?** (This habit - interrogating your own measurements - is what Month 2 turns into a discipline.)

### Week-specific additions:
- **Week 1:** Where in the call lifecycle did your intuition turn out to be wrong? (Did the first token arrive sooner or later than you expected? Was cold-start a bigger factor than you thought?)
- **Week 2:** What's the most uncomfortable consequence of "an LLM call is not idempotent" that you hadn't considered before this week?
- **Week 3:** How wrong was your cost estimate before you fixed the tokenizer - and did that number change how much you'll trust *any* usage field going forward?
- **Week 4:** If you had to defend your "route to cloud above complexity X" threshold to a skeptical architect tomorrow, which part of your evidence is weakest?

---

# "What This Month Sets Up"

You now have the slab - the measurement instrument the entire remaining 17 months stands on. Specifically:

- **Month 2 (Evaluation-Driven Development)** doesn't talk to OpenAI or Ollama directly - it calls *your* `client.complete()`. Every eval result inherits your telemetry for free, and "QUALITY" graduates from this month's crude parse-failure rate into a real coding-task pass rate scored by deterministic checks + a calibrated AI-as-judge. Your fixed-prompt-set, error-bars, never-a-bare-number discipline *is* the eval discipline - you've already started practicing it.

- **Month 3 (Your First AI Coding Agent)** is built on this client. The agent is just a loop that calls `generate()` repeatedly - and every one of those calls is already measured, retried, and logged. The agent inherits resilience for free.

- **Month 6 (Tool Use & Side Effects)** is where the "LLM calls aren't idempotent" lesson stops being a print statement and starts mattering for real - when a retried call could double-apply a file edit. You've already thought it through in the Week 2 drill.

- **Month 10 (Cost-Aware Routing)** sits directly on top of this month's local-vs-cloud table and your first routing threshold. The router is the formalization of the rule you wrote in Lab 8.

- **Month 13 (Observability)** reads the *same* telemetry log you built this month, just at production scale with a real backend. The schema you chose in Week 3 is the schema the dashboard renders.

If you skipped this month - if you went straight to building the agent on top of a framework you didn't understand - you'd have no baseline, no way to attribute cost, no way to prove an optimization helped, and no way to trace a failure. You'd be tuning prompts on vibes and claiming improvements you can't defend. You did the unsexy work of building the instrument first. Now everything you build on top of it is measurable. That's the difference between an AI hobbyist and an AI engineer.

*- End of Month 1 lesson plan. No call without telemetry. No claim without a number. Build the dumb, measured version before the smart one. The instrument comes first - everything else stands on it.*
