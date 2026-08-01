import json
import time

import httpx


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


# available model list: mistral:latest, llama3.1:latest
def raw_generate(prompt: str, model: str = "mistral:latest"):
    url = "http://localhost:11434/api/generate"
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
    with httpx.stream("POST", url, json=payload, timeout=120) as r:
        for line in r.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
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
    print(f"{prompt}")
    print("------------answer-----------------")
    print("".join(response_parts))

    return extract_metrics(
        time_to_first_token_seconds,
        total_elapsed_seconds,
        final_response_chunk,
    )


if __name__ == '__main__':
    prompt = "Explain agentic AI in 2 sentences."
    metrics = raw_generate(prompt)

    print("-------------metrics----------------")
    for name, value in metrics.items():
        print(f"{name}: {value}")
