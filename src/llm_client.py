"""Thin Gemini wrapper. The agent only depends on the two-method LLMClient
interface, so tests can pass a fake. Only music preferences and song metadata
should ever be sent through this module (free-tier prompts may be used by Google).
"""

import json
import os
import time
from pathlib import Path
from typing import Optional

DEFAULT_MODEL = "gemini-3.5-flash-lite"
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


class LLMUnavailable(Exception):
    """Raised for a missing key, API error, rate limit or unparseable output."""


class LLMClient:
    """Interface the agent uses. Subclass or duck-type it in tests."""

    def generate_json(self, prompt: str, schema: dict) -> dict:
        raise NotImplementedError

    def generate_text(self, prompt: str) -> str:
        raise NotImplementedError


class GeminiClient(LLMClient):
    def __init__(self, model: Optional[str] = None, max_retries: int = 2,
                 base_delay: float = 2.0, timeout_s: int = 30):
        self.model = model or os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.timeout_s = timeout_s
        self._client = None
        self.calls = 0

    def _get_client(self):
        if self._client is None:
            try:
                from dotenv import load_dotenv
                load_dotenv(ENV_PATH)
            except ImportError:
                pass
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                raise LLMUnavailable("GEMINI_API_KEY is not set")
            try:
                from google import genai
                from google.genai import types
            except ImportError as exc:
                raise LLMUnavailable("google-genai is not installed") from exc
            self._client = genai.Client(
                api_key=key,
                # http timeout is in milliseconds; retries are handled here.
                http_options=types.HttpOptions(
                    timeout=self.timeout_s * 1000,
                    retry_options=types.HttpRetryOptions(attempts=1),
                ),
            )
        return self._client

    def _call(self, prompt: str, schema: Optional[dict]) -> str:
        from google.genai import errors, types

        client = self._get_client()
        config = types.GenerateContentConfig(temperature=0.2)
        if schema is not None:
            config = types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_json_schema=schema,
            )
        last: Exception = LLMUnavailable("unknown error")
        for attempt in range(self.max_retries + 1):
            try:
                self.calls += 1
                resp = client.models.generate_content(
                    model=self.model, contents=prompt, config=config
                )
                text = resp.text
                if not text:
                    raise LLMUnavailable("empty response")
                return text
            except LLMUnavailable as exc:
                last = exc
            except errors.APIError as exc:
                last = LLMUnavailable(f"API error {getattr(exc, 'code', '?')}")
                code = getattr(exc, "code", 0) or 0
                if 400 <= code < 500 and code != 429:
                    break  # bad request / auth: retrying will not help
            except Exception as exc:  # network, timeout, SDK internals
                last = LLMUnavailable(f"{type(exc).__name__}")
            if attempt < self.max_retries:
                time.sleep(self.base_delay * (2 ** attempt))
        raise last

    def generate_json(self, prompt: str, schema: dict) -> dict:
        text = self._call(prompt, schema)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMUnavailable("invalid JSON from model") from exc
        if not isinstance(data, dict):
            raise LLMUnavailable("JSON response is not an object")
        return data

    def generate_text(self, prompt: str) -> str:
        return self._call(prompt, None).strip()
