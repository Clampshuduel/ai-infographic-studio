"""RenderJob: the unit of work passed through the pipeline."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class RenderJob:
    id: str
    source: Path
    spec_name: str
    created_at: datetime
    output_format: str = "png"
    tags: dict[str, str] = field(default_factory=dict)
    attempts: int = 0

    @classmethod
    def new(cls, source: Path, spec_name: str = "auto", output_format: str = "png") -> "RenderJob":
        return cls(
            id=uuid.uuid4().hex[:12],
            source=Path(source),
            spec_name=spec_name,
            created_at=datetime.now(timezone.utc),
            output_format=output_format,
        )