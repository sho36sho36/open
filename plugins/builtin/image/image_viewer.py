from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QMovie,
    QPixmap,
    QTransform,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ImageViewer(QWidget):
    """一般的な画像ファイル用のビューア。"""

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info

        self.original_pixmap = QPixmap()
        self.display_pixmap = QPixmap()

        self.movie = None

        self.zoom = 1.0
        self.rotation = 0

        self.fit_mode = True

        self._build_ui()
        self._load_file()

    def _build_ui(self):
        self.setMinimumSize(
            700,
            500,
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setSpacing(8)

        header = QHBoxLayout()

        self.title_label = QLabel(
            self.file_info.name
        )

        self.title_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        self.title_label.setWordWrap(True)

        header.addWidget(
            self.title_label,
            1,
        )

        self.info_label = QLabel(
            ""
        )

        self.info_label.setStyleSheet(
            """
            QLabel {
                color: #888888;
                font-size: 12px;
            }
            """
        )

        header.addWidget(
            self.info_label
        )

        layout.addLayout(
            header
        )

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        self.scroll_area.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.image_label = QLabel()

        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.image_label.setStyleSheet(
            """
            QLabel {
                background: #202020;
            }
            """
        )

        self.image_label.setMinimumSize(
            1,
            1,
        )

        self.scroll_area.setWidget(
            self.image_label
        )

        layout.addWidget(
            self.scroll_area,
            1,
        )

        controls = QHBoxLayout()

        self.zoom_out_button = QPushButton(
            "🔍−"
        )

        self.zoom_label = QLabel(
            "100%"
        )

        self.zoom_in_button = QPushButton(
            "🔍＋"
        )

        self.fit_button = QPushButton(
            "↔ 画面に合わせる"
        )

        self.rotate_left_button = QPushButton(
            "↶ 左回転"
        )

        self.rotate_right_button = QPushButton(
            "↷ 右回転"
        )

        controls.addStretch()

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

        controls.addWidget(
            self.rotate_left_button
        )

        controls.addWidget(
            self.rotate_right_button
        )

        controls.addStretch()

        layout.addLayout(
            controls
        )

        self.status_label = QLabel(
            "読み込み中..."
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #777777;
            }
            """
        )

        layout.addWidget(
            self.status_label
        )

        self.zoom_out_button.clicked.connect(
            self.zoom_out
        )

        self.zoom_in_button.clicked.connect(
            self.zoom_in
        )

        self.fit_button.clicked.connect(
            self.fit_to_window
        )

        self.rotate_left_button.clicked.connect(
            self.rotate_left
        )

        self.rotate_right_button.clicked.connect(
            self.rotate_right
        )

    def _load_file(self):
        path = Path(
            self.file_info.path
        )

        if not path.exists():
            self.status_label.setText(
                "ファイルが存在しません。"
            )
            return

        if not path.is_file():
            self.status_label.setText(
                "ファイルではありません。"
            )
            return

        extension = path.suffix.lower()

        if extension == ".gif":
            self._load_gif(path)
            return

        pixmap = QPixmap(
            str(path)
        )

        if pixmap.isNull():
            self.status_label.setText(
                "画像を読み込めませんでした。"
            )
            return

        self.original_pixmap = pixmap

        self.info_label.setText(
            self._format_info(
                pixmap.width(),
                pixmap.height(),
            )
        )

        self.status_label.setText(
            "画像を読み込みました。"
        )

        self.fit_to_window()

    def _load_gif(self, path):
        self.movie = QMovie(
            str(path)
        )

        if not self.movie.isValid():
            self.status_label.setText(
                "GIFを読み込めませんでした。"
            )
            return

        self.image_label.setMovie(
            self.movie
        )

        self.movie.start()

        size = self.movie.currentImage().size()

        self.info_label.setText(
            self._format_info(
                size.width(),
                size.height(),
            )
            + "    GIF"
        )

        self.status_label.setText(
            "GIFアニメーション再生中"
        )

        self.fit_mode = True

    def _format_info(
        self,
        width,
        height,
    ):
        size = self.file_info.size

        if size < 1024:
            size_text = f"{size} B"

        elif size < 1024 * 1024:
            size_text = (
                f"{size / 1024:.1f} KB"
            )

        else:
            size_text = (
                f"{size / (1024 * 1024):.1f} MB"
            )

        extension = (
            self.file_info.extension.upper()
        )

        return (
            f"{width} × {height}    "
            f"{extension}    "
            f"{size_text}"
        )

    def zoom_in(self):
        if self.movie is not None:
            return

        self.fit_mode = False

        self.zoom = min(
            self.zoom * 1.25,
            20.0,
        )

        self._update_image()

    def zoom_out(self):
        if self.movie is not None:
            return

        self.fit_mode = False

        self.zoom = max(
            self.zoom / 1.25,
            0.05,
        )

        self._update_image()

    def fit_to_window(self):
        if self.movie is not None:
            self.fit_mode = True
            return

        if self.original_pixmap.isNull():
            return

        self.fit_mode = True

        viewport_size = (
            self.scroll_area.viewport().size()
        )

        available_width = max(
            1,
            viewport_size.width() - 10,
        )

        available_height = max(
            1,
            viewport_size.height() - 10,
        )

        image_width = (
            self.original_pixmap.width()
        )

        image_height = (
            self.original_pixmap.height()
        )

        scale_x = (
            available_width
            / image_width
        )

        scale_y = (
            available_height
            / image_height
        )

        self.zoom = min(
            scale_x,
            scale_y,
            1.0,
        )

        self._update_image()

    def rotate_left(self):
        if self.movie is not None:
            return

        self.rotation = (
            self.rotation - 90
        ) % 360

        self._update_image()

    def rotate_right(self):
        if self.movie is not None:
            return

        self.rotation = (
            self.rotation + 90
        ) % 360

        self._update_image()

    def _update_image(self):
        if self.movie is not None:
            return

        if self.original_pixmap.isNull():
            return

        transform = QTransform()

        transform.rotate(
            self.rotation
        )

        rotated = (
            self.original_pixmap.transformed(
                transform,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        width = max(
            1,
            int(
                rotated.width()
                * self.zoom
            ),
        )

        height = max(
            1,
            int(
                rotated.height()
                * self.zoom
            ),
        )

        self.display_pixmap = (
            rotated.scaled(
                width,
                height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        self.image_label.setPixmap(
            self.display_pixmap
        )

        self.image_label.resize(
            self.display_pixmap.size()
        )

        self.zoom_label.setText(
            f"{self.zoom * 100:.0f}%"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.fit_mode:
            self.fit_to_window()

    def closeEvent(self, event):
        if self.movie is not None:
            self.movie.stop()
            self.movie = None

        self.image_label.clear()

        super().closeEvent(event)