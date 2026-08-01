import json
import logging
import time

import httpx

logger = logging.getLogger(__name__)

# Fallback context limit for models whose metadata is not listed below.
MODEL_CONTEXT_LIMIT = 32_768

# Context lengths observed locally with `ollama show <model>` on 2026-08-01.
MODEL_CONTEXT_LIMITS = {
    "mistral:latest": 32_768,
    "qwen2.5-coder:7b": 32_768,
    "llama3.1:latest": 131_072,
}

# Lab 2 observation:
# Sending ~40 000 estimated tokens to local model via Ollama:
# → Ollama silently truncated the FRONT of the prompt (system instructions lost).
# → No error returned; response looked normal but was generated from a mangled context.
# → Behavior changed at ~33 000 estimated tokens (≈ 132 000 chars).
# This is the "silent corruption" bug the guard below is designed to prevent.


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: chars ÷ 4, rounded up. Good enough for a pre-flight guard;
    replace with a real tokenizer in Week 3."""
    return (len(text) + 3) // 4


def _context_limit_for_model(
    model: str,
    model_context_limit: int | None = None,
) -> int:
    """Return an explicit, known, or fallback context limit for a model."""
    if model_context_limit is not None:
        if model_context_limit <= 0:
            raise ValueError("model_context_limit must be a positive integer.")
        return model_context_limit
    return MODEL_CONTEXT_LIMITS.get(model, MODEL_CONTEXT_LIMIT)


def _preflight_guard(
    prompt: str,
    model_context_limit: int = MODEL_CONTEXT_LIMIT,
    truncate: bool = True,
) -> str:
    """Estimate prompt tokens and either truncate or refuse if over the limit.

    Args:
        prompt: The prompt string to check.
        model_context_limit: Maximum tokens the model can accept.
        truncate: If True, trim the front of the prompt and return the remainder.
                  If False, raise ValueError so the caller must handle it.

    Returns:
        The (possibly truncated) prompt that is safe to send.

    Raises:
        ValueError: When truncate=False and the prompt exceeds the limit.
    """
    if model_context_limit <= 0:
        raise ValueError("model_context_limit must be a positive integer.")

    estimated = _estimate_tokens(prompt)
    if estimated <= model_context_limit:
        return prompt

    if truncate:
        # Keep only the tail so that the most-recent context survives.
        # A char budget of (limit * 4) preserves the prompt end.
        char_budget = model_context_limit * 4
        truncated_prompt = prompt[-char_budget:]
        logger.warning(
            "[preflight_guard] Prompt too large: ~%d tokens estimated, "
            "limit %d. TRUNCATED front %d chars (lost ~%d tokens). "
            "Sending tail only.",
            estimated,
            model_context_limit,
            len(prompt) - char_budget,
            estimated - model_context_limit,
        )
        return truncated_prompt
    else:
        logger.error(
            "[preflight_guard] Prompt too large: ~%d tokens estimated, "
            "limit %d. REFUSED — not sending.",
            estimated,
            model_context_limit,
        )
        raise ValueError(
            f"Prompt exceeds context limit: ~{estimated} tokens estimated, "
            f"limit is {model_context_limit}. Refusing to send."
        )


def extract_metrics(
    time_to_first_token_seconds: float | None,
    total_elapsed_seconds: float,
    final_response_chunk: dict,
) -> dict:
    prompt_tokens = final_response_chunk.get("prompt_eval_count", 0)
    completion_tokens = final_response_chunk.get("eval_count", 0)
    eval_duration_ns = final_response_chunk.get("eval_duration", 0)
    eval_duration_s = eval_duration_ns / 1e9
    tokens_per_sec = (
        completion_tokens / eval_duration_s if eval_duration_s else 0.0
    )

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "ttft_ms": (time_to_first_token_seconds or 0.0) * 1000,
        "total_ms": total_elapsed_seconds * 1000,
        "tokens_per_sec": tokens_per_sec,
    }


# available model list: mistral:latest, llama3.1:latest, qwen2.5-coder:7b
def raw_generate(
    prompt: str,
    model: str = "mistral:latest",
    truncate_on_overflow: bool = True,
    bypass_guard: bool = False,
    model_context_limit: int | None = None,
):
    url = "http://localhost:11434/api/generate"
    context_limit = _context_limit_for_model(model, model_context_limit)
    if bypass_guard:
        logger.info(
            "[preflight_guard] BYPASSED — sending prompt as-is (~%d tokens estimated, "
            "limit %d for %s).",
            _estimate_tokens(prompt),
            context_limit,
            model,
        )
    else:
        prompt = _preflight_guard(
            prompt,
            model_context_limit=context_limit,
            truncate=truncate_on_overflow,
        )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {"temperature": 0},
    }
    request_started_at = time.perf_counter()
    time_to_first_token_seconds = None
    final_response_chunk = {}
    response_parts = []
    with httpx.stream("POST", url, json=payload, timeout=300) as r:
        for line in r.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            if "error" in chunk:
                raise RuntimeError(f"Ollama error: {chunk['error']}")
            response = chunk.get("response")
            if response:
                response_parts.append(response)
            if time_to_first_token_seconds is None and response:
                time_to_first_token_seconds = time.perf_counter() - request_started_at
            if chunk.get("done"):
                final_response_chunk = chunk
    total_elapsed_seconds = time.perf_counter() - request_started_at

    # debug purpose
    print("------------prompt-----------------")
    # print(f"{prompt}")
    print("------------answer-----------------")
    print("".join(response_parts))

    return extract_metrics(
        time_to_first_token_seconds,
        total_elapsed_seconds,
        final_response_chunk,
    )


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")

    # ── Build an oversized prompt ──────────────────────────────────────────────
    # Filler repeated 4 000× ≈ ~180 000 chars before the question;
    # total ≈ 45 000 estimated tokens — well over the 32 768 limit.
    # After truncation, Test 1 sends only the model-sized tail.
    filler = "The quick brown fox jumps over the lazy dog. " * 4_000
    oversized = filler + "\n\nIgnoring all the text above, answer in one sentence: what is 2 + 2?"
    estimated = _estimate_tokens(oversized)
    print(f"Oversized prompt: {len(oversized):,} chars ≈ {estimated:,} estimated tokens")
    print(f"Model context limit: {_context_limit_for_model('mistral:latest'):,} tokens\n")

    # ── Test 1: truncate mode (default) ───────────────────────────────────────
    print("=== Test 1: truncate_on_overflow=True (guard truncates, then sends) ===")
    try:
        metrics = raw_generate(oversized, model="mistral:latest", truncate_on_overflow=True)
        print("\n-------------metrics----------------")
        for name, value in metrics.items():
            print(f"{name}: {value}")
    except Exception as e:
        print(f"Error in Test 1: {e}", file=sys.stderr)

    print()

    # ── Test 2: refuse mode ────────────────────────────────────────────────────
    print("=== Test 2: truncate_on_overflow=False (guard refuses, no request sent) ===")
    try:
        raw_generate(oversized, model="mistral:latest", truncate_on_overflow=False)
        print("ERROR: should have raised ValueError but did not!", file=sys.stderr)
    except ValueError as e:
        print(f"Guard raised ValueError as expected:\n  {e}")

    print()

    # ── Test 3: bypass guard entirely ─────────────────────────────────────────
    # Use this to observe raw Ollama behavior when the context limit is exceeded.
    # WARNING: Ollama may silently truncate the FRONT of the prompt.
    print("=== Test 3: bypass_guard=True (no guard — raw Ollama behavior) ===")
    print("Watch prompt_tokens in metrics: if it's < estimated, Ollama truncated silently.\n")
    try:
        metrics = raw_generate(oversized, model="mistral:latest", bypass_guard=True)
        print("\n-------------metrics----------------")
        for name, value in metrics.items():
            print(f"{name}: {value}")
        actual_prompt_tokens = metrics.get("prompt_tokens", 0)
        print(f"\n[guard bypassed] estimated={estimated:,} vs ollama_prompt_tokens={actual_prompt_tokens:,}")
        if actual_prompt_tokens < estimated:
            print("⚠  Ollama silently truncated the prompt (front likely lost).")
        else:
            print("✓  Ollama accepted the full prompt.")
    except RuntimeError as e:
        print(f"Ollama returned an error (no silent truncation this time): {e}")
    except Exception as e:
        print(f"Error in Test 3: {e}", file=sys.stderr)
