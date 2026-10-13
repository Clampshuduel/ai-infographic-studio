"""Qt main window: dataset picker, spec editor, render queue panel."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ai_infographic_studio.models.job import RenderJob
from ai_infographic_studio.services.queue import RenderQueue
from ai_infographic_studio.utils.log import get_logger

log = get_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, cfg) -> None:
        super().__init__()
        self.cfg = cfg
        self.queue = RenderQueue(max_workers=cfg.render.workers)
        self.setWindowTitle(f"AI Infographic Studio {cfg.version}")
        self.resize(1180, 760)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(QLabel("Dataset:"))
        self.dataset_label = QLabel("<none selected>")
        layout.addWidget(self.dataset_label)

        row = QHBoxLayout()
        pick = QPushButton("Open dataset…")
        pick.clicked.connect(self._pick_dataset)
        render = QPushButton("Render infographic")
        render.clicked.connect(self._render)
        row.addWidget(pick)
        row.addWidget(render)
        layout.addLayout(row)

        layout.addStretch(1)
        self.setCentralWidget(root)
        self._dataset: Path | None = None

    def _pick_dataset(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open dataset",
            "",
            "Datasets (*.csv *.json *.xlsx *.md);;All files (*)",
        )
        if path:
            self._dataset = Path(path)
            self.dataset_label.setText(str(self._dataset))

    def _render(self) -> None:
        if self._dataset is None:
            log.warning("render_clicked_no_dataset")
            return
        job = RenderJob.new(source=self._dataset, spec_name="auto")
        self.queue.submit(job)
        log.info("job_submitted", job_id=job.id, source=str(self._dataset))