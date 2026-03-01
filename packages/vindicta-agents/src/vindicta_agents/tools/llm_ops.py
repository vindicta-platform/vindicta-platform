"""LLM operations — Ollama provider implementing the LLMProvider protocol.

Wraps the ``ollama`` Python package for local model inference.
The default model is configurable via the ``OLLAMA_MODEL`` environment
variable (falls back to ``mistral``).
"""

from __future__ import annotations

import json
import os
from typing import Any

import ollama as _ollama_pkg


class OllamaLLMProvider:
    """LLM provider backed by a local Ollama instance.

    Parameters
    ----------
    model:
        Ollama model name.  Defaults to ``OLLAMA_MODEL`` env var or
        ``"mistral"``.
    host:
        Ollama server URL.  Defaults to ``OLLAMA_HOST`` env var or
        ``"http://localhost:11434"``.
    """

    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
    ) -> None:
        self.model = model or os.environ.get("OLLAMA_MODEL", "mistral")
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self._client = _ollama_pkg.Client(host=self.host)

    # ---- text generation ----

    def generate_text(
        self,
        prompt: str,
        *,
        system: str = "",
        model: str | None = None,
    ) -> str:
        """Generate a text completion.

        Returns the model's response as a plain string.
        """
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat(
            model=model or self.model,
            messages=messages,
        )
        return response["message"]["content"]

    # ---- structured JSON generation ----

    def generate_json(
        self,
        prompt: str,
        *,
        system: str = "",
        model: str | None = None,
    ) -> dict[str, Any]:
        """Generate a JSON response.

        Instructs the model to reply in JSON and parses the result.
        Returns a Python dict.
        """
        json_system = (
            system + "\n\n" if system else ""
        ) + "You MUST respond with valid JSON only. No markdown, no explanation."
        raw = self.generate_text(
            prompt,
            system=json_system,
            model=model,
        )
        # Strip markdown code fences if the model wraps output
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first and last lines (code fence markers)
            lines = [line for line in lines if not line.strip().startswith("```")]
            cleaned = "\n".join(lines)
        return json.loads(cleaned)
