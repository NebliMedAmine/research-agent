"""Tool stubs for the agent: search, code, retrieval.

Fill these in with real implementations or connectors to external services.
"""
from typing import Any


def search(query: str) -> list[dict[str, Any]]:
    """Search tool stub.

    Returns an empty list. Implement search over your index/data source.
    """
    raise NotImplementedError("search() is not implemented")


def code(query: str) -> dict[str, Any]:
    """Code generation/help tool stub.

    Implement code generation or retrieval helpers here.
    """
    raise NotImplementedError("code() is not implemented")


def retrieve(document_id: str) -> dict[str, Any]:
    """Retrieval tool stub for documents.

    Implement retrieval from vector DB or file store.
    """
    raise NotImplementedError("retrieve() is not implemented")


__all__ = ["search", "code", "retrieve"]
