"""FastAPI entrypoint for Insight2Spec."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Application factory for easier testing and future config injection."""
    app = FastAPI(title="Insight2Spec API", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        """Lightweight liveness probe."""
        return {"status": "ok", "service": "insight2spec"}

    return app


app = create_app()
