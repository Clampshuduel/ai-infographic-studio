"""Config loader: default.yaml -> user.yaml -> env overrides."""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from ai_infographic_studio import __version__
from ai_infographic_studio.utils.paths import user_config_dir


class LLMConfig(BaseModel):
    backend: str = "local"          # local | openai | anthropic | ollama
    model: str = "llama3.1:8b"
    api_key_ref: str = "ai-infographic-studio/openai"
    timeout_s: float = 60.0
    max_retries: int = 3


class RenderConfig(BaseModel):
    workers: int = Field(default=4, ge=1, le=32)
    dpi: int = Field(default=220, ge=72, le=600)
    default_format: str = "png"
    output_dir: Path = Field(default_factory=lambda: Path.home() / "Pictures" / "ai-infographic-studio")


class AppConfig(BaseModel):
    version: str = __version__
    log_level: str = "INFO"
    telemetry_opt_in: bool = False
    llm: LLMConfig = LLMConfig()
    render: RenderConfig = RenderConfig()


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_config() -> AppConfig:
    defaults = Path(__file__).with_name("default.yaml")
    merged = _load_yaml(defaults)
    merged.update(_load_yaml(user_config_dir() / "user.yaml"))
    if env_level := os.environ.get("AIIS_LOG_LEVEL"):
        merged["log_level"] = env_level
    return AppConfig.model_validate(merged)