from pathlib import Path

import pymupdf

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QImage,
    QPixmap,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class PDFViewer(QWidget):
    """PDFファイル表示用ビューア。"""

    MIN_ZOOM = 25
    MAX_ZOOM = 400
    DEFAULT_ZOOM = 100
    ZOOM_STEP = 25

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info
        self.file_path = Path(
            file_info.path
        )

        self.document = None
        self.current_page = 0
        self.zoom = self.DEFAULT_ZOOM

        self.setWindowTitle(
            f"{file_info.name} - open"
        )

        self._build_ui()
        self._open_document()

    def _build_ui(self):
        self.page_label = QLabel(
            self
        )

        self.page_label.setAlignment(
            Qt.AlignCenter
        )

        self.page_label.setMinimumWidth(
            100
        )

        self.zoom_label = QLabel(
            "100%",
            self,
        )

        self.info_label = QLabel(
            self
        )

        self.info_label.setAlignment(
            Qt.AlignCenter
        )

        self.previous_button = QPushButton(
            "◀ 前のページ",
            self,
        )

        self.next_button = QPushButton(
            "次のページ ▶",
            self,
        )

        self.zoom_out_button = QPushButton(
            "－",
            self,
        )

        self.zoom_in_button = QPushButton(
            "＋",
            self,
        )

        self.fit_button = QPushButton(
            "幅に合わせる",
            self,
        )

        self.page_spin = QSpinBox(
            self
        )

        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(1)

        self.previous_button.clicked.connect(
            self._previous_page
        )

        self.next_button.clicked.connect(
            self._next_page
        )

        self.zoom_out_button.clicked.connect(
            self._zoom_out
        )

        self.zoom_in_button.clicked.connect(
            self._zoom_in
        )

        self.fit_button.clicked.connect(
            self._fit_width
        )

        self.page_spin.valueChanged.connect(
            self._page_changed
        )

        controls = QHBoxLayout()

        controls.addWidget(
            self.previous_button
        )

        controls.addWidget(
            self.page_spin
        )

        controls.addWidget(
            self.next_button
        )

        controls.addSpacing(
            15
        )

        controls.addWidget(
            self.zoom_out_button
        )

        controls.addWidget(
            self.zoom_label
        )

        controls.addWidget(
            self.zoom_in_button
        )

        controls.addWidget(
            self.fit_button
        )

        controls.addStretch(
            1
        )

        controls.addWidget(
            self.info_label
        )

        self.scroll_area = QScrollArea(
            self
        )

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setAlignment(
            Qt.AlignCenter
        )

        self.scroll_area.setWidget(
            self.page_label
        )

        layout = QVBoxLayout(
            self
        )

        layout.addLayout(
            controls
        )

        layout.addWidget(
            self.scroll_area,
            1,
        )

    def _open_document(self):
        try:
            self.document = pymupdf.open(
                str(self.file_path)
            )

        except Exception as exc:
            self.page_label.setText(
                "PDFを開けませんでした。\n\n"
                f"{exc}"
            )

            self.previous_button.setEnabled(
                False
            )

            self.next_button.setEnabled(
                False
            )

            self.page_spin.setEnabled(
                False
            )

            return

        page_count = self.document.page_count

        if page_count <= 0:
            self.page_label.setText(
                "PDFにページがありません。"
            )

            return

        self.page_spin.setMaximum(
            page_count
        )

        self.info_label.setText(
            f"{self.file_info.name}"
            f"  |  {page_count} ページ"
            f"  |  {self._format_size(self.file_info.size)}"
        )

        self._update_page()

    def _update_page(self):
        if self.document is None:
            return

        if not (
            0
            <= self.current_page
            < self.document.page_count
        ):
            return

        page = self.document.load_page(
            self.current_page
        )

        scale = self.zoom / 100.0

        matrix = pymupdf.Matrix(
            scale,
            scale,
        )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format_RGB888,
        )

        pixmap_qt = QPixmap.fromImage(
            image.copy()
        )

        self.page_label.setPixmap(
            pixmap_qt
        )

        self.page_label.resize(
            pixmap_qt.size()
        )

        self.page_spin.blockSignals(
            True
        )

        self.page_spin.setValue(
            self.current_page + 1
        )

        self.page_spin.blockSignals(
            False
        )

        self.zoom_label.setText(
            f"{self.zoom}%"
        )

        self.previous_button.setEnabled(
            self.current_page > 0
        )

        self.next_button.setEnabled(
            self.current_page
            < self.document.page_count - 1
        )

    def _previous_page(self):
        if self.current_page <= 0:
            return

        self.current_page -= 1
        self._update_page()

        self._scroll_to_top()

    def _next_page(self):
        if self.document is None:
            return

        if (
            self.current_page
            >= self.document.page_count - 1
        ):
            return

        self.current_page += 1
        self._update_page()

        self._scroll_to_top()

    def _page_changed(self, value):
        if self.document is None:
            return

        page_index = value - 1

        if not (
            0
            <= page_index
            < self.document.page_count
        ):
            return

        self.current_page = page_index
        self._update_page()

        self._scroll_to_top()

    def _zoom_in(self):
        self.zoom = min(
            self.MAX_ZOOM,
            self.zoom + self.ZOOM_STEP,
        )

        self._update_page()

    def _zoom_out(self):
        self.zoom = max(
            self.MIN_ZOOM,
            self.zoom - self.ZOOM_STEP,
        )

        self._update_page()

    def _fit_width(self):
        if self.document is None:
            return

        page = self.document.load_page(
            self.current_page
        )

        page_width = page.rect.width

        if page_width <= 0:
            return

        available_width = (
            self.scroll_area.viewport().width()
            - 20
        )

        if available_width <= 0:
            return

        self.zoom = max(
            self.MIN_ZOOM,
            min(
                self.MAX_ZOOM,
                int(
                    available_width
                    / page_width
                    * 100
                ),
            ),
        )

        self._update_page()

    def _scroll_to_top(self):
        vertical_scrollbar = (
            self.scroll_area.verticalScrollBar()
        )

        vertical_scrollbar.setValue(
            vertical_scrollbar.minimum()
        )

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} B"

        if size < 1024 * 1024:
            return (
                f"{size / 1024:.1f} KB"
            )

        if size < 1024 * 1024 * 1024:
            return (
                f"{size / (1024 * 1024):.1f} MB"
            )

        return (
            f"{size / (1024 * 1024 * 1024):.1f} GB"
        )

    def closeEvent(self, event):
        if self.document is not None:
            self.document.close()
            self.document = None

        super().closeEvent(event)