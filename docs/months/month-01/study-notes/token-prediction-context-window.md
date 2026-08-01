## Token, Prediction, Context Window
### What a token is
- A token is the atomic unit of text that the model sees; it is usually a sub‑word fragment, not necessarily a full word.

- Modern LLMs use subword tokenization (e.g., “running” → “run”, “##ing”), so a single English word may become several tokens, and spaces, punctuation, and partial words all count as tokens.

### What “next‑token prediction” means (and why outputs differ)
- The core training objective is: given all previous tokens in a sequence, predict the next token with a probability distribution over the vocabulary.

- At inference time, the model samples from this distribution rather than always taking the single most likely token; different random samples (or different decoding settings like temperature, top‑k/top‑p) produce different next tokens, so the same input can yield different continuations.

### Why the context window is a hard, finite budget
- The model can only attend to a fixed‑length sequence of tokens at once (its context window), which is like a bounded “working memory” used for both your prompt and its own generated text.

- This limit is hard because the transformer’s computation and memory scale with the square of the number of tokens; beyond a certain size, it becomes too expensive or impossible to run, so every token you add consumes a piece of that finite budget.

### Concrete Examples
**Token vs word: a 4-token sentence**

Take the short sentence:

> “I love Saigon!”

Using a typical subword tokenizer like the ones used in LLMs, this might become 4 tokens:

- `I`

- `love` (leading space is part of the token)

- `Sai`

- `gon!`

So:

- The model doesn’t see “Saigon” as one unit; it sees the subword pieces " Sai" and "gon!".

- A “4k‑token” context window would hold around 4,000 such fragments, not 4,000 words; depending on language and punctuation, that might be roughly 2,000–3,000 words of actual text.

**Next‑token prediction with different outputs**

Extend the text to:

> “I love Saigon because”

Suppose the model’s next‑token probability distribution looks roughly like this:

- `it` – 40%

- `of` – 25%

- `the` – 15%

- `it's` – 10%

- other tokens – 10% total

Two different decoding choices:

- Deterministic (greedy) decoding

  - Always pick the highest‑probability token.

  - The model will consistently continue with `it` → `I love Saigon because it …`.

- Sampling with temperature

  - Treat the probabilities like a dice roll and sample.

  - One run: you might get `of` → `I love Saigon because of …`.

  - Another run with the same input and settings: you might get `it's` → `I love Saigon because it's …`.

So:

- The training objective is always “given previous tokens, predict the next token distribution,” but at generation time you can either pick the top token or sample, and sampling is what makes the same prompt produce different outputs across runs.

**Context window as a hard budget (4k vs 128k)**
Imagine 2 models:

- Model A: 4k‑token context window

- Model B: 128k‑token context window

You give each one a long document + your question:

- The document: ~100 pages of text about economics (≈ 100k tokens).

- Your question at the end: `Summarize the three main causes of inflation discussed above.`

What happens?

- Model A (4k) can only “see” roughly the last 4k tokens when predicting the next token.

  - If your question and only the last few pages fit into 4k, it literally cannot attend to the earlier chapters; they are outside its working memory.

  - It might give a summary based only on the last section, ignoring crucial earlier causes.

- Model B (128k) can attend to nearly the whole 100k‑token document plus your question.

  - It can pull information from chapters near the beginning, middle, and end in a single forward pass.

**Why is this a hard limit?**

- Internally, the transformer does attention over all tokens in the context; the compute and memory cost grows at least linearly, and often roughly with the square of the number of tokens (more tokens → much more work).

- Beyond the designed window (e.g., >4k or >128k), the model simply does not compute attention for those tokens, so they might as well not exist; that’s why Karpathy calls the context window a “finite precious resource of working memory.”

Putting it together for intuition:

- Think of each token as a little tile of text; a 4k window is like a strip of 4,000 tiles the model can see at once.

- Next‑token prediction is: “Given the current strip of tiles, choose the next tile according to a probability distribution,” and sampling makes the sequence branch differently each time.

- The strip length (context window) is fixed by design and hardware budgets, so anything outside it is invisible during that prediction step, which is why you feel the limit so sharply when prompts or documents get long.
