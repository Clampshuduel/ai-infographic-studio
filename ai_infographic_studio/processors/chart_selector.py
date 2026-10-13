"""ChartSelector: picks chart types per chart node based on data shape."""
from __future__ import annotations

from ai_infographic_studio.models.canvas import Canvas
from ai_infographic_studio.models.dataset import Dataset
from ai_infographic_studio.processors.base import Processor


class ChartSelector(Processor):
    name = "chart_selector"

    def apply(self, dataset: Dataset, canvas: Canvas) -> Canvas:
        numeric = [c.name for c in dataset.columns if c.dtype == "numeric"]
        categorical = [c.name for c in dataset.columns if c.dtype == "categorical"]
        temporal = [c.name for c in dataset.columns if c.dtype == "temporal"]

        for node in canvas.walk():
            if node.kind != "chart":
                continue
            if temporal and numeric:
                node.payload.update({"chart": "line", "x": temporal[0], "y": numeric[0]})
            elif categorical and numeric:
                node.payload.update({"chart": "bar", "x": categorical[0], "y": numeric[0]})
            elif len(numeric) >= 2:
                node.payload.update({"chart": "scatter", "x": numeric[0], "y": numeric[1]})
            else:
                node.payload.update({"chart": "table"})
        return canvas