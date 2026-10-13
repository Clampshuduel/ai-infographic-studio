"""PNG driver: rasterizes the Canvas via matplotlib."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ai_infographic_studio.drivers.base import OutputDriver  # noqa: E402
from ai_infographic_studio.models.canvas import Canvas  # noqa: E402
from ai_infographic_studio.models.job import RenderJob  # noqa: E402


class PngDriver(OutputDriver):
    format = "png"

    def render(self, job: RenderJob, canvas: Canvas, out_path: Path) -> Path:
        dpi = 160
        fig = plt.figure(
            figsize=(canvas.width / dpi, canvas.height / dpi),
            dpi=dpi,
            facecolor=canvas.background,
        )
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, canvas.width)
        ax.set_ylim(canvas.height, 0)
        ax.axis("off")

        for node in canvas.walk():
            if node.kind == "text":
                ax.text(
                    node.x, node.y + node.h * 0.6, node.payload.get("text", ""),
                    color="#e6edf3", fontsize=22, weight="bold", va="top",
                )
            elif node.kind == "chart":
                ax.add_patch(plt.Rectangle(
                    (node.x, node.y), node.w, node.h,
                    fill=False, edgecolor=canvas.palette[0] if canvas.palette else "#30363d",
                    lw=1.5,
                ))
                ax.text(
                    node.x + node.w / 2, node.y + node.h / 2,
                    node.payload.get("chart", "chart"),
                    color="#8b949e", fontsize=14, ha="center", va="center",
                )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=dpi, facecolor=canvas.background)
        plt.close(fig)
        return out_path