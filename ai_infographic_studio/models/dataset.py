"""Dataset: normalized tabular payload produced by ingest handlers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Column:
    name: str
    dtype: str          # "numeric" | "categorical" | "temporal" | "text"
    null_ratio: float = 0.0
    distinct: int = 0


@dataclass(slots=True)
class Dataset:
    columns: list[Column]
    rows: list[dict[str, Any]]
    source_kind: str = "unknown"
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def n_rows(self) -> int:
        return len(self.rows)

    @property
    def n_cols(self) -> int:
        return len(self.columns)