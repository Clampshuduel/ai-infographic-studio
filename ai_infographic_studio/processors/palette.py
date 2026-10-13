"""PaletteProcessor: derives a color scheme from brand or content."""
from __future__ import annotations

import colorsys

from ai_infographic_studio.models.canvas import Canvas
from ai_infographic_studio.models.dataset import Dataset
from ai_infographic_studio.processors.base import Processor

_SEEDS = {
    "finance": "#1f6feb",
    "health": "#2ea043",
    "climate": "#3fb950",
    "marketing": "#db61a2",
    "default": "#a371f7",
}


def _rotate(hex_color: str, hue_shift: float, n: int = 5) -> list[str]:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    out = []
    for i in range(n):
        hh = (h + hue_shift * i) % 1.0
        rr, gg, bb = colorsys.hsv_to_rgb(hh, s, v)
        out.append(f"#{int(rr * 255):02x}{int(gg * 255):02x}{int(bb * 255):02x}")
    return out


class PaletteProcessor(Processor):
    name = "palette"

    def apply(self, dataset: Dataset, canvas: Canvas) -> Canvas:
        domain = str(dataset.meta.get("domain", "default")).lower()
        seed = _SEEDS.get(domain, _SEEDS["default"])
        canvas.palette = _rotate(seed, hue_shift=0.08, n=5)
        return canvas