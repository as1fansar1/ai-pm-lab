import httpx
import pytest

from app.openrouter_client import (
    OpenRouterClient,
    OpenRouterConfigError,
    OpenRouterRequestError,
    OpenRouterTimeoutError,
)


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict | None = None, text: str = "") -> None:
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self) -> dict:
        return self._payload


class _FakeClient:
    def __init__(self, *, response: _FakeResponse | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error

    def __enter__(self) -> "_FakeClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def post(self, *args, **kwargs):
        if self.error:
            raise self.error
        return self.response


def test_from_env_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(OpenRouterConfigError):
        OpenRouterClient.from_env()


def test_complete_json_returns_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = {"id": "abc", "choices": [{"message": {"content": "hi"}}]}

    monkeypatch.setattr(
        "app.openrouter_client.httpx.Client",
        lambda timeout: _FakeClient(response=_FakeResponse(200, expected)),
    )

    client = OpenRouterClient(api_key="test-key")
    result = client.complete_json(
        model="openai/gpt-4o-mini",
        system_prompt="You are helpful.",
        user_prompt="Say hi",
    )

    assert result == expected


def test_complete_json_maps_http_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.openrouter_client.httpx.Client",
        lambda timeout: _FakeClient(response=_FakeResponse(429, text="rate limited")),
    )

    client = OpenRouterClient(api_key="test-key")

    with pytest.raises(OpenRouterRequestError):
        client.complete_json(
            model="openai/gpt-4o-mini",
            system_prompt="You are helpful.",
            user_prompt="Say hi",
        )


def test_complete_json_maps_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.openrouter_client.httpx.Client",
        lambda timeout: _FakeClient(error=httpx.TimeoutException("timed out")),
    )

    client = OpenRouterClient(api_key="test-key", timeout_seconds=0.1)

    with pytest.raises(OpenRouterTimeoutError):
        client.complete_json(
            model="openai/gpt-4o-mini",
            system_prompt="You are helpful.",
            user_prompt="Say hi",
        )
