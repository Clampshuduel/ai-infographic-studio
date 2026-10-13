"""Base class for ingest handlers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ai_infographic_studio.models.dataset import Dataset


class IngestHandler(ABC):
    """Pure: file bytes/text in, normalized Dataset out."""

    name: str = "base"
    suffixes: tuple[str, ...] = ()

    @abstractmethod
    def can_handle(self, path: Path) -> bool: ...

    @abstractmethod
    def load(self, path: Path) -> Dataset: ...