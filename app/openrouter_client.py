"""Minimal OpenRouter client wrapper for Insight2Spec."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterError(Exception):
    """Base error for OpenRouter client failures."""


class OpenRouterConfigError(OpenRouterError):
    """Raised when required configuration is missing."""


class OpenRouterRequestError(OpenRouterError):
    """Raised when OpenRouter rejects a request."""


class OpenRouterTimeoutError(OpenRouterError):
    """Raised when a request to OpenRouter times out."""


@dataclass(slots=True)
class OpenRouterClient:
    """Small typed wrapper around OpenRouter Chat Completions API."""

    api_key: str
    timeout_seconds: float = 20.0
    base_url: str = OPENROUTER_BASE_URL
    app_name: str = "Insight2Spec"

    @classmethod
    def from_env(cls) -> "OpenRouterClient":
        """Build client from environment variables.

        Required:
            OPENROUTER_API_KEY

        Optional:
            OPENROUTER_TIMEOUT_SECONDS
        """
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise OpenRouterConfigError("OPENROUTER_API_KEY is required")

        timeout_seconds = float(os.getenv("OPENROUTER_TIMEOUT_SECONDS", "20"))
        return cls(api_key=api_key, timeout_seconds=timeout_seconds)

    def complete_json(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        """Call OpenRouter chat completions and return raw JSON payload."""
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://insight2spec.local",
            "X-Title": self.app_name,
        }

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
        except httpx.TimeoutException as exc:
            raise OpenRouterTimeoutError(
                f"OpenRouter request timed out after {self.timeout_seconds}s"
            ) from exc
        except httpx.HTTPError as exc:
            raise OpenRouterRequestError("OpenRouter request failed before response") from exc

        if response.status_code >= 400:
            raise OpenRouterRequestError(
                f"OpenRouter returned HTTP {response.status_code}: {response.text[:300]}"
            )

        return response.json()
