"""FastAPI entrypoint for research-agent backend."""
from fastapi import FastAPI
import os


def create_app() -> FastAPI:
    app = FastAPI(title="research-agent backend")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    # Run with: `uvicorn backend.main:app --reload --port 8000`
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
