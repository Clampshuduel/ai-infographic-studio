"""Base class for output drivers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ai_infographic_studio.models.canvas import Canvas
from ai_infographic_studio.models.job import RenderJob


class OutputDriver(ABC):
    format: str = "base"

    @abstractmethod
    def render(self, job: RenderJob, canvas: Canvas, out_path: Path) -> Path: ...