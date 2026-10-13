"""Entry point for the desktop app.

Boots config, registers built-in handlers/processors/drivers, then
hands control to the Qt main loop.
"""
from __future__ import annotations

import sys

from ai_infographic_studio.app.window import MainWindow
from ai_infographic_studio.config.loader import load_config
from ai_infographic_studio.drivers import registry as driver_registry
from ai_infographic_studio.ingest import registry as ingest_registry
from ai_infographic_studio.processors import registry as proc_registry
from ai_infographic_studio.utils.log import get_logger, setup_logging


def build_app() -> int:
    cfg = load_config()
    setup_logging(cfg.log_level)
    log = get_logger(__name__)
    log.info("boot", version=cfg.version, backend=cfg.llm.backend)

    ingest_registry.register_builtins()
    proc_registry.register_builtins()
    driver_registry.register_builtins()

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow(cfg)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(build_app())