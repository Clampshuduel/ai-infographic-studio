"""Base class for processors."""
from __future__ import annotations

from abc import ABC, abstractmethod

from ai_infographic_studio.models.canvas import Canvas
from ai_infographic_studio.models.dataset import Dataset


class Processor(ABC):
    name: str = "base"

    @abstractmethod
    def apply(self, dataset: Dataset, canvas: Canvas) -> Canvas: ...