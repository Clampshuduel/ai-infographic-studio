"""LayoutPlanner: chooses layout template from data shape + spec."""
from __future__ import annotations

from ai_infographic_studio.models.canvas import Canvas, Node
from ai_infographic_studio.models.dataset import Dataset
from ai_infographic_studio.processors.base import Processor
from ai_infographic_studio.utils.log import get_logger

log = get_logger(__name__)


class LayoutPlanner(Processor):
    name = "layout_planner"

    def apply(self, dataset: Dataset, canvas: Canvas) -> Canvas:
        n_numeric = sum(1 for c in dataset.columns if c.dtype == "numeric")
        n_cat = sum(1 for c in dataset.columns if c.dtype == "categorical")

        if n_numeric >= 3 and n_cat >= 1:
            template = "hero_plus_three"
        elif n_numeric >= 1:
            template = "single_hero"
        else:
            template = "text_grid"

        log.info("layout_selected", template=template, rows=dataset.n_rows)

        margin = int(canvas.width * 0.04)
        header_h = int(canvas.height * 0.18)
        canvas.root = Node(kind="panel", x=0, y=0, w=canvas.width, h=canvas.height,
                           payload={"template": template})
        canvas.root.children.append(Node(
            kind="text", x=margin, y=margin,
            w=canvas.width - 2 * margin, h=header_h,
            payload={"role": "title", "text": dataset.meta.get("title", "Infographic")},
        ))
        canvas.root.children.append(Node(
            kind="chart", x=margin, y=margin + header_h,
            w=canvas.width - 2 * margin, h=canvas.height - header_h - 2 * margin,
            payload={"role": "primary"},
        ))
        return canvas