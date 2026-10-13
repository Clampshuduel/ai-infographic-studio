"""Markdown -> Dataset. Extracts tables and headline stats from prose."""
from __future__ import annotations

import re
from pathlib import Path

from ai_infographic_studio.ingest.base import IngestHandler
from ai_infographic_studio.models.dataset import Column, Dataset

_TABLE_ROW = re.compile(r"^\|(.+)\|$")


class MarkdownHandler(IngestHandler):
    name = "markdown"
    suffixes = (".md", ".markdown")

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.suffixes

    def load(self, path: Path) -> Dataset:
        lines = path.read_text(encoding="utf-8").splitlines()
        header: list[str] | None = None
        rows: list[dict] = []
        for line in lines:
            m = _TABLE_ROW.match(line.strip())
            if not m:
                continue
            cells = [c.strip() for c in m.group(1).split("|")]
            if header is None:
                header = cells
                continue
            if all(set(c) <= {"-", ":", " "} for c in cells):
                continue
            rows.append(dict(zip(header, cells, strict=False)))
        if header is None:
            raise ValueError(f"{path}: no markdown tables found")
        columns = [Column(name=h, dtype="text", distinct=len({r.get(h) for r in rows})) for h in header]
        return Dataset(columns=columns, rows=rows, source_kind="markdown", meta={"path": str(path)})