## Chip Huyen – *AI Engineering* (Ch. 1–2)
### Working Vocabulary (API-Focused)

The goal is to understand each term well enough to know **which API parameter it maps to** when making LLM requests.

| Term | Definition | API Parameter | What you'll use this week |
|------|------------|---------------|----------------------------|
| **Context window** | The maximum amount of text the model can process in one request. It includes your prompt, conversation history, retrieved documents, and the model's response. | Indirectly managed by your prompt size and `max_tokens` (or `max_completion_tokens`). | Keep prompts concise and ensure **input + output** fit within the model's context window. |
| **Tokens** | The basic units of text processed by the model. Tokens are not the same as words. Every request consumes input tokens and generates output tokens. | `max_tokens` (or `max_completion_tokens`) | Set an upper limit for response length and estimate cost based on token usage. |
| **Temperature** | Controls randomness during text generation. Lower values produce more deterministic responses; higher values produce more diverse and creative responses. | `temperature` | Use **0.0–0.2** for coding, extraction, and structured outputs. Use **0.7–1.0** for brainstorming or creative writing. |
| **Top_p** | Uses nucleus sampling to limit the candidate tokens to the smallest set whose cumulative probability reaches `p`. | `top_p` | Usually leave at **1.0** unless you specifically want to experiment. Most APIs recommend adjusting either `temperature` or `top_p`, not both. |
| **Sampling** | The process the model uses to choose the next token from its probability distribution. Temperature and top_p influence this process. | No direct parameter. Controlled by `temperature` and `top_p`. | Understand it as the mechanism behind text generation rather than a parameter you send. |

---

### Example API Request

```json
{
  "model": "your-model",
  "messages": [
    {
      "role": "user",
      "content": "Explain Kubernetes in simple terms."
    }
  ],
  "temperature": 0.2,
  "top_p": 1.0,
  "max_tokens": 500
}
```

---

### Practical Defaults

For most backend AI applications:

```json
{
  "temperature": 0.2,
  "top_p": 1.0,
  "max_tokens": 1000
}
```

This configuration provides:

- Predictable responses
- Good performance for coding and automation
- Easier debugging
- A solid baseline before tuning parameters

---

### Quick Memory Guide

| Term | Remember it as... |
|------|--------------------|
| **Context window** | How much the model can remember in one request. |
| **Tokens** | The units you pay for and fit into the context window. |
| **Temperature** | How creative or deterministic the model should be. |
| **Top_p** | How many likely next-token candidates the model considers. |
| **Sampling** | The process of choosing the next token using the probability distribution. |

---

### API Parameter Mapping

| Concept | Parameter You'll Send |
|----------|-----------------------|
| Response creativity | `temperature` |
| Alternative randomness control | `top_p` |
| Maximum response length | `max_tokens` |
| Prompt size | Your application controls it |
| Context window | Determined by the model; managed by prompt size + `max_tokens` |
| Sampling | Not sent directly; influenced by `temperature` and `top_p` |