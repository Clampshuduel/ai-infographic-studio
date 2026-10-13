"""SVG driver: serializes Canvas to SVG via a tag/attribute allowlist."""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, select_autoescape

from ai_infographic_studio.drivers.base import OutputDriver
from ai_infographic_studio.models.canvas import Canvas
from ai_infographic_studio.models.job import RenderJob
from ai_infographic_studio.utils.log import get_logger

log = get_logger(__name__)

_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {{ w }} {{ h }}" width="{{ w }}" height="{{ h }}">
  <rect width="{{ w }}" height="{{ h }}" fill="{{ bg }}"/>
  {%- for node in nodes %}
  {%- if node.kind == 'text' %}
  <text x="{{ node.x }}" y="{{ node.y + node.h * 0.6 }}" fill="#e6edf3"
        font-family="Inter, Segoe UI, sans-serif" font-size="24" font-weight="700">{{ node.text }}</text>
  {%- elif node.kind == 'chart' %}
  <rect x="{{ node.x }}" y="{{ node.y }}" width="{{ node.w }}" height="{{ node.h }}"
        fill="none" stroke="{{ stroke }}" stroke-width="1.5"/>
  <text x="{{ node.x + node.w / 2 }}" y="{{ node.y + node.h /