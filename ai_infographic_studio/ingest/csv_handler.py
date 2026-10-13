"""CSV -> Dataset. Uses pandas for type inference, then narrows dtypes."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from ai_infographic_studio.ingest.base import IngestHandler
from ai_infographic_studio.models.dataset import Column, Dataset


def _infer_dtype(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "temporal"
    return "categorical" if series.nunique(dropna=True) <= 64 else "text"


class CsvHandler(IngestHandler):
    name = "csv"
    suffixes = (".csv", ".tsv")

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.suffixes

    def load(self, path: Path) -> Dataset:
        sep = "\t" if path.suffix.lower() == ".tsv" else ","
        df = pd.read_csv(path, sep=sep, engine="python")
        columns = [
            Column(
                name=str(col),
                dtype=_infer_dtype(df[col]),
                null_ratio=float(df[col].isna().mean()),
                distinct=int(df[col].nunique(dropna=True)),
            )
            for col in df.columns
        ]
        rows = df.where(df.notna(), None).to_dict(orient="records")
        return Dataset(columns=columns, rows=rows, source_kind="csv", meta={"path": str(path)})