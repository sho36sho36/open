import io
import re
import zipfile

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtSvgWidgets import QSvgWidget


class DesignViewer(QWidget):
    """デザイン・ベクターファイルを表示するViewer。"""

    SUPPORTED_EXTENSIONS = {
        ".svg",
        ".eps",
        ".ai",
        ".psd",
        ".xcf",
        ".kra",
    }

    IMAGE_EXTENSIONS = {
        ".psd",
        ".xcf",
        ".kra",
    }

    VECTOR_EXTENSIONS = {
        ".svg",
        ".eps",
        ".ai",
    }

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info
        self.path = Path(file_info.path)

        self.current_pixmap = None
        self.svg_widget = None

        self.preview_label = QLabel()
        self.info_label = QLabel()

        self.layer_list = QListWidget()

        self.reload_button = QPushButton(
            "再読み込み"
        )

        self.fit_button = QPushButton(
            "画面に合わせる"
        )

        self._setup_ui()
        self._load_file()

    # ==================================================
    # UI
    # ==================================================

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        title = QLabel(
            f"🎨 Design Viewer - {self.path.name}"
        )

        title.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        header_layout.addWidget(title)
        header_layout.addStretch()

        header_layout.addWidget(
            self.fit_button
        )

        header_layout.addWidget(
            self.reload_button
        )

        main_layout.addLayout(
            header_layout
        )

        main_layout.addWidget(
            self.info_label
        )

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        preview_container = QWidget()

        preview_layout = QVBoxLayout(
            preview_container
        )

        self.preview_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.preview_label.setText(
            "プレビューを読み込んでいます..."
        )

        self.preview_label.setMinimumSize(
            300,
            250,
        )

        self.preview_label.setStyleSheet(
            """
            QLabel {
                background: #202124;
                color: #ffffff;
                border: 1px solid #555555;
            }
            """
        )

        preview_layout.addWidget(
            self.preview_label
        )

        splitter.addWidget(
            preview_container
        )

        layer_container = QWidget()

        layer_layout = QVBoxLayout(
            layer_container
        )

        layer_title = QLabel(
            "レイヤー / ファイル情報"
        )

        layer_layout.addWidget(
            layer_title
        )

        self.layer_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        layer_layout.addWidget(
            self.layer_list
        )

        splitter.addWidget(
            layer_container
        )

        splitter.setStretchFactor(
            0,
            4,
        )

        splitter.setStretchFactor(
            1,
            1,
        )

        main_layout.addWidget(
            splitter
        )

        self.reload_button.clicked.connect(
            self._load_file
        )

        self.fit_button.clicked.connect(
            self._fit_preview
        )

    # ==================================================
    # Load
    # ==================================================

    def _load_file(self):
        extension = self.path.suffix.lower()

        self.layer_list.clear()

        self._clear_preview()

        if extension not in self.SUPPORTED_EXTENSIONS:
            self._show_error(
                "対応していないデザイン形式です。"
            )
            return

        try:
            if extension == ".svg":
                self._load_svg()

            elif extension == ".eps":
                self._load_eps()

            elif extension == ".ai":
                self._load_ai()

            elif extension == ".psd":
                self._load_psd()

            elif extension == ".xcf":
                self._load_xcf()

            elif extension == ".kra":
                self._load_kra()

        except Exception as exc:
            self._show_error(
                "ファイルを読み込めませんでした。",
                exc,
            )

    # ==================================================
    # SVG
    # ==================================================

    def _load_svg(self):
        widget = QSvgWidget()

        widget.load(
            str(self.path)
        )

        self.svg_widget = widget

        self._replace_preview(
            widget
        )

        file_size = self.path.stat().st_size

        self.info_label.setText(
            f"SVG / "
            f"{file_size:,} bytes"
        )

        self._add_layer(
            "SVG",
            "ベクター画像",
        )

    # ==================================================
    # EPS
    # ==================================================

    def _load_eps(self):
        try:
            from PIL import Image

        except ImportError as exc:
            raise RuntimeError(
                "EPSの表示にはPillowが必要です。"
            ) from exc

        try:
            image = Image.open(
                self.path
            )

            image.load()

            pixmap = self._pil_to_pixmap(
                image
            )

            self._set_pixmap(
                pixmap
            )

            self.info_label.setText(
                f"EPS / "
                f"{image.width} × "
                f"{image.height}"
            )

            self._add_layer(
                "EPS",
                "ベクター画像プレビュー",
            )

        except Exception as exc:
            raise RuntimeError(
                "EPSを画像として読み込めませんでした。\n"
                "環境によってはGhostscriptなどの"
                "外部レンダラーが必要です。"
            ) from exc

    # ==================================================
    # AI
    # ==================================================

    def _load_ai(self):
        data = self.path.read_bytes()

        pdf_index = data.find(
            b"%PDF-"
        )

        if pdf_index < 0:
            self.preview_label.setText(
                "このAIファイルには\n"
                "PDF互換プレビューがありません。"
            )

            self.info_label.setText(
                "AI / PDF互換データなし"
            )

            self._add_layer(
                "AI",
                "Adobe Illustrator",
            )

            return

        try:
            import pymupdf

            document = pymupdf.open(
                stream=data[pdf_index:],
                filetype="pdf",
            )

            if document.page_count == 0:
                raise RuntimeError(
                    "PDFページがありません。"
                )

            page = document.load_page(
                0
            )

            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(
                    1.5,
                    1.5,
                ),
                alpha=False,
            )

            pixmap = QPixmap()

            pixmap.loadFromData(
                pix.tobytes("png"),
                "PNG",
            )

            self._set_pixmap(
                pixmap
            )

            self.info_label.setText(
                f"AI / "
                f"PDF互換プレビュー / "
                f"{document.page_count}ページ"
            )

            self._add_layer(
                "AI",
                "Illustrator PDF互換プレビュー",
            )

            document.close()

        except Exception as exc:
            raise RuntimeError(
                "AIのPDF互換データを"
                "表示できませんでした。"
            ) from exc

    # ==================================================
    # PSD
    # ==================================================

    def _load_psd(self):
        try:
            from PIL import Image

        except ImportError as exc:
            raise RuntimeError(
                "PSDの表示にはPillowが必要です。"
            ) from exc

        with Image.open(
            self.path
        ) as image:
            image.load()

            pixmap = self._pil_to_pixmap(
                image
            )

            self._set_pixmap(
                pixmap
            )

            self.info_label.setText(
                f"PSD / "
                f"{image.width} × "
                f"{image.height}"
            )

            self._add_layer(
                "PSD",
                f"{image.width} × "
                f"{image.height}",
            )

            self._extract_psd_layers(
                image
            )

    def _extract_psd_layers(
        self,
        image,
    ):
        try:
            layers = getattr(
                image,
                "layers",
                None,
            )

            if layers:
                for index, layer in enumerate(
                    layers,
                    start=1,
                ):
                    name = getattr(
                        layer,
                        "name",
                        None,
                    )

                    if name:
                        self._add_layer(
                            f"{index}. {name}",
                            "PSD Layer",
                        )

        except Exception:
            pass

    # ==================================================
    # XCF
    # ==================================================

    def _load_xcf(self):
        try:
            from PIL import Image

        except ImportError as exc:
            raise RuntimeError(
                "XCFの表示にはPillowが必要です。"
            ) from exc

        try:
            with Image.open(
                self.path
            ) as image:
                image.load()

                pixmap = self._pil_to_pixmap(
                    image
                )

                self._set_pixmap(
                    pixmap
                )

                self.info_label.setText(
                    f"XCF / "
                    f"{image.width} × "
                    f"{image.height}"
                )

                self._add_layer(
                    "XCF",
                    f"{image.width} × "
                    f"{image.height}",
                )

                self._extract_pillow_layers(
                    image
                )

        except Exception as exc:
            raise RuntimeError(
                "XCFのプレビューを"
                "読み込めませんでした。\n"
                "このXCFの構造によっては"
                "GIMPなどの専用ソフトが必要です。"
            ) from exc

    # ==================================================
    # KRA
    # ==================================================

    def _load_kra(self):
        if not zipfile.is_zipfile(
            self.path
        ):
            raise RuntimeError(
                "KRAファイルとして認識できません。"
            )

        with zipfile.ZipFile(
            self.path,
            "r",
        ) as archive:

            names = archive.namelist()

            preview_candidates = [
                "mergedimage.png",
                "preview.png",
                "preview/preview.png",
            ]

            preview_name = None

            for candidate in preview_candidates:
                if candidate in names:
                    preview_name = candidate
                    break

            if preview_name is None:
                for name in names:
                    lower = name.lower()

                    if (
                        lower.endswith(
                            "mergedimage.png"
                        )
                        or lower.endswith(
                            "preview.png"
                        )
                    ):
                        preview_name = name
                        break

            if preview_name is None:
                raise RuntimeError(
                    "KRA内にプレビュー画像がありません。"
                )

            data = archive.read(
                preview_name
            )

            pixmap = QPixmap()

            if not pixmap.loadFromData(
                data,
                "PNG",
            ):
                raise RuntimeError(
                    "KRAプレビューを"
                    "画像として読み込めませんでした。"
                )

            self._set_pixmap(
                pixmap
            )

            self.info_label.setText(
                f"KRA / "
                f"プレビュー: "
                f"{preview_name}"
            )

            self._add_layer(
                "KRA",
                "Krita document",
            )

            self._extract_kra_layers(
                archive,
                names,
            )

    def _extract_kra_layers(
        self,
        archive,
        names,
    ):
        if "maindoc.xml" not in names:
            return

        try:
            data = archive.read(
                "maindoc.xml"
            ).decode(
                "utf-8",
                errors="replace",
            )

            names_found = re.findall(
                r'name="([^"]+)"',
                data,
            )

            unique_names = []

            for name in names_found:
                if name not in unique_names:
                    unique_names.append(
                        name
                    )

            for name in unique_names:
                self._add_layer(
                    name,
                    "Krita Layer",
                )

        except Exception:
            pass

    # ==================================================
    # Preview
    # ==================================================

    def _set_pixmap(
        self,
        pixmap,
    ):
        self.current_pixmap = pixmap

        self._fit_preview()

    def _fit_preview(self):
        if self.current_pixmap is None:
            return

        if self.current_pixmap.isNull():
            return

        size = self.preview_label.size()

        scaled = self.current_pixmap.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.preview_label.setPixmap(
            scaled
        )

    def _replace_preview(
        self,
        widget,
    ):
        layout = self.preview_label.parentWidget().layout()

        if layout is None:
            return

        index = layout.indexOf(
            self.preview_label
        )

        if index < 0:
            return

        self.preview_label.hide()

        layout.insertWidget(
            index,
            widget,
        )

    def _clear_preview(self):
        if self.svg_widget is not None:
            self.svg_widget.deleteLater()
            self.svg_widget = None

        self.current_pixmap = None

        self.preview_label.clear()

        self.preview_label.setText(
            "プレビューを読み込んでいます..."
        )

        self.preview_label.show()

    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _pil_to_pixmap(
        image,
    ):
        if image.mode not in (
            "RGB",
            "RGBA",
        ):
            image = image.convert(
                "RGBA"
            )

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="PNG",
        )

        pixmap = QPixmap()

        pixmap.loadFromData(
            buffer.getvalue(),
            "PNG",
        )

        return pixmap

    def _add_layer(
        self,
        name,
        description,
    ):
        item = QListWidgetItem(
            f"👁 {name}"
        )

        item.setToolTip(
            description
        )

        self.layer_list.addItem(
            item
        )

    def _extract_pillow_layers(
        self,
        image,
    ):
        try:
            layers = getattr(
                image,
                "layers",
                None,
            )

            if not layers:
                return

            for index, layer in enumerate(
                layers,
                start=1,
            ):
                name = getattr(
                    layer,
                    "name",
                    None,
                )

                if name:
                    self._add_layer(
                        f"{index}. {name}",
                        "Layer",
                    )

        except Exception:
            pass

    def _show_error(
        self,
        message,
        exception=None,
    ):
        if exception is not None:
            message = (
                f"{message}\n\n"
                f"{exception}"
            )

        self.info_label.setText(
            message
        )

        self.preview_label.setText(
            message
        )

        QMessageBox.warning(
            self,
            "Design / Vector Plugin",
            message,
        )

    # ==================================================
    # Resize
    # ==================================================

    def resizeEvent(
        self,
        event,
    ):
        super().resizeEvent(
            event
        )

        self._fit_preview()