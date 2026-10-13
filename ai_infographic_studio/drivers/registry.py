"""Driver registry + built-in registration."""
from __future__ import annotations

from ai_infographic_studio.drivers.base import OutputDriver

DRIVER_REGISTRY: dict[str, OutputDriver] = {}


def register(driver: OutputDriver) -> OutputDriver:
    DRIVER_REGISTRY[driver.format] = driver
    return driver


def resolve(fmt: str) -> OutputDriver:
    if fmt not in DRIVER_REGISTRY:
        raise LookupError(f"no driver for format {fmt!r}")
    return DRIVER_REGISTRY[fmt]


def register_builtins() -> None:
    from ai_infographic_studio.drivers.png_driver import PngDriver
    from ai_infographic_studio.drivers.svg_driver import SvgDriver

    register(PngDriver())
    register(SvgDriver())