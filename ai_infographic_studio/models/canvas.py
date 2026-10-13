"""Canvas: abstract layout tree consumed by output drivers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

NodeKind = Literal["panel", "text", "chart", "image", "divider"]


@dataclass(slots=True)
class Node:
    kind: NodeKind
    x: float
    y: float
    w: float
    h: float
    payload: dict = field(default_factory=dict)
    children: list["Node"] = field(default_factory=list)


@dataclass(slots=True)
class Canvas:
    width: int
    height: int
    background: str = "#0e1116"
    palette: list[str] = field(default_factory=list)
    root: Node | None = None

    def walk(self):
        stack = [self.root] if self.root else []
        while stack:
            node = stack.pop()
            yield node
            stack.extend(node.children)