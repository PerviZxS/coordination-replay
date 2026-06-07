"""Interface to the local Qwen3 model served by Ollama.

A single async function that sends a prompt to the Ollama HTTP API at
temperature 0 and returns the model's text response. Temperature 0 makes the
output near-deterministic, so that across repeated runs the response content
is effectively constant and the only thing that varies is the wall-clock time
each call takes. That variable latency is the real source of interaction-order
nondeterminism the experiment measures.
"""

import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:0.6b"


async def ask_model(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0},
    }
    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"].strip()