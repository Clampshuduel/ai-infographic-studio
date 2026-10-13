"""Handler registry + built-in registration."""
from __future__ import annotations

from ai_infographic_studio.ingest.base import IngestHandler

HANDLER_REGISTRY: dict[str, IngestHandler] = {}


def register(handler: IngestHandler) -> IngestHandler:
    HANDLER_REGISTRY[handler.name] = handler
    return handler


def resolve(path) -> IngestHandler:
    for handler in HANDLER_REGISTRY.values():
        if handler.can_handle(path):
            return handler
    raise LookupError(f"no ingest handler for {path}")


def register_builtins() -> None:
    from ai_infographic_studio.ingest.csv_handler import CsvHandler
    from ai_infographic_studio.ingest.json_handler import JsonHandler
    from ai_infographic_studio.ingest.markdown_handler import MarkdownHandler

    register(CsvHandler())
    register(JsonHandler())
    register(MarkdownHandler())