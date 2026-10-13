"""JSON -> Dataset. Accepts list-of-objects or {rows: [...]}."""
from __future__ import annotations

import json
from pathlib import Path

from ai_infographic_studio.ingest.base import IngestHandler
from ai_infographic_studio.models.dataset import Column, Dataset


class JsonHandler(IngestHandler):
    name = "json"
    suffixes = (".json",)

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.suffixes

    def load(self, path: Path) -> Dataset:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("rows") if isinstance(payload, dict) else payload
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"{path}: expected non-empty list of objects")
        keys = list({k for row in rows for k in row.keys()})
        columns = [
            Column(
                name=k,
                dtype="numeric" if all(isinstance(r.get(k), (int, float)) for r in rows) else "text",
                null_ratio=sum(1 for r in rows if r.get(k) is None) / len(rows),
                distinct=len({r.get(k) for r in rows}),
            )
            for k in keys
        ]
        return Dataset(columns=columns, rows=rows, source_kind="json", meta={"path": str(path)})