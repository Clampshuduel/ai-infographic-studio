"""Processor registry + built-in registration."""
from __future__ import annotations

from ai_infographic_studio.processors.base import Processor

PROCESSOR_REGISTRY: dict[str, Processor] = {}


def register(processor: Processor) -> Processor:
    PROCESSOR_REGISTRY[processor.name] = processor
    return processor


def register_builtins() -> None:
    from ai_infographic_studio.processors.chart_selector import ChartSelector
    from ai_infographic_studio.processors.layout_planner import LayoutPlanner
    from ai_infographic_studio.processors.palette import PaletteProcessor

    register(LayoutPlanner())
    register(ChartSelector())
    register(PaletteProcessor())