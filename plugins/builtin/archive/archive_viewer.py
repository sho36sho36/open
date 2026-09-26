import mimetypes
import zipfile
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ArchiveViewer(QWidget):
    """ZIPファイル表示・展開用ビューア。"""

    TEXT_EXTENSIONS = {
        ".txt",
        ".log",
        ".csv",
        ".tsv",
        ".ini",
        ".cfg",
        ".conf",
        ".md",
        ".markdown",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".toml",
        ".py",
        ".pyw",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".html",
        ".htm",
        ".css",
        ".scss",
        ".sass",
        ".less",
        ".java",
        ".kt",
        ".kts",
        ".c",
        ".h",
        ".cpp",
        ".cc",
        ".cxx",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".swift",
        ".dart",
        ".lua",
        ".rb",
        ".php",
        ".sql",
        ".sh",
        ".bash",
        ".zsh",
        ".bat",
        ".cmd",
        ".ps1",
    }

    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".webp",
        ".tiff",
        ".tif",
        ".ico",
    }

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

        self.archive = None
        self.entries = []

        self.setWindowTitle(
            f"{file_info.name} - open"
        )

        self._build_ui()
        self._open_archive()

    def _build_ui(self):
        self.info_label = QLabel(
            self
        )

        self.info_label.setText(
            "ZIPファイルを読み込んでいます..."
        )

        self.extract_button = QPushButton(
            "📦 すべて展開",
            self,
        )

        self.extract_button.clicked.connect(
            self._extract_all
        )

        self.extract_selected_button = QPushButton(
            "📄 選択項目を展開",
            self,
        )

        self.extract_selected_button.clicked.connect(
            self._extract_selected
        )

        self.refresh_button = QPushButton(
            "🔄 更新",
            self,
        )

        self.refresh_button.clicked.connect(
            self._refresh
        )

        top_layout = QHBoxLayout()

        top_layout.addWidget(
            self.info_label,
            1,
        )

        top_layout.addWidget(
            self.extract_selected_button
        )

        top_layout.addWidget(
            self.extract_button
        )

        top_layout.addWidget(
            self.refresh_button
        )

        self.tree = QTreeWidget(
            self
        )

        self.tree.setHeaderLabels(
            [
                "名前",
                "種類",
                "サイズ",
                "圧縮後",
            ]
        )

        self.tree.setColumnWidth(
            0,
            320,
        )

        self.tree.itemSelectionChanged.connect(
            self._selection_changed
        )

        self.preview = QTextEdit(
            self
        )

        self.preview.setReadOnly(
            True
        )

        self.preview.setPlaceholderText(
            "ファイルを選択すると詳細を表示します。"
        )

        self.preview_image = QLabel(
            self
        )

        self.preview_image.setAlignment(
            Qt.AlignCenter
        )

        self.preview_image.setMinimumSize(
            200,
            200,
        )

        self.preview_image.setText(
            "画像を選択するとここに表示されます。"
        )

        self.preview_image.setWordWrap(
            True
        )

        self.preview_stack = QWidget(
            self
        )

        preview_layout = QVBoxLayout(
            self.preview_stack
        )

        preview_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        preview_layout.addWidget(
            self.preview
        )

        preview_layout.addWidget(
            self.preview_image
        )

        self.preview_image.hide()

        splitter = QSplitter(
            Qt.Horizontal,
            self,
        )

        splitter.addWidget(
            self.tree
        )

        splitter.addWidget(
            self.preview_stack
        )

        splitter.setStretchFactor(
            0,
            2,
        )

        splitter.setStretchFactor(
            1,
            3,
        )

        layout = QVBoxLayout(
            self
        )

        layout.addLayout(
            top_layout
        )

        layout.addWidget(
            splitter,
            1,
        )

    def _open_archive(self):
        try:
            self.archive = zipfile.ZipFile(
                self.file_path,
                "r",
            )

            self.entries = (
                self.archive.infolist()
            )

        except Exception as exc:
            self.info_label.setText(
                "ZIPファイルを開けませんでした。"
            )

            QMessageBox.critical(
                self,
                "open",
                "ZIPファイルを開けませんでした。\n\n"
                f"{exc}",
            )

            self.extract_button.setEnabled(
                False
            )

            self.extract_selected_button.setEnabled(
                False
            )

            return

        file_count = sum(
            not entry.is_dir()
            for entry in self.entries
        )

        directory_count = sum(
            entry.is_dir()
            for entry in self.entries
        )

        total_size = sum(
            entry.file_size
            for entry in self.entries
            if not entry.is_dir()
        )

        self.info_label.setText(
            f"{self.file_info.name}"
            f"  |  {file_count} ファイル"
            f"  |  {directory_count} フォルダ"
            f"  |  {self._format_size(total_size)}"
        )

        self._build_tree()

    def _build_tree(self):
        self.tree.clear()

        root = self.tree.invisibleRootItem()

        directory_items = {
            "": root,
        }

        for entry in self.entries:
            path = entry.filename.replace(
                "\\",
                "/",
            ).strip("/")

            if not path:
                continue

            parts = [
                part
                for part in path.split("/")
                if part
            ]

            current_path = ""

            parent_item = root

            for index, part in enumerate(
                parts
            ):
                current_path = (
                    f"{current_path}/{part}"
                    if current_path
                    else part
                )

                is_last = (
                    index
                    == len(parts) - 1
                )

                if (
                    not is_last
                    or entry.is_dir()
                ):
                    if (
                        current_path
                        not in directory_items
                    ):
                        item = QTreeWidgetItem(
                            parent_item
                        )

                        item.setText(
                            0,
                            part,
                        )

                        item.setText(
                            1,
                            "フォルダ",
                        )

                        item.setData(
                            0,
                            Qt.UserRole,
                            current_path,
                        )

                        directory_items[
                            current_path
                        ] = item

                    parent_item = (
                        directory_items[
                            current_path
                        ]
                    )

                    continue

                item = QTreeWidgetItem(
                    parent_item
                )

                item.setText(
                    0,
                    part,
                )

                item.setText(
                    1,
                    "ファイル",
                )

                item.setText(
                    2,
                    self._format_size(
                        entry.file_size
                    ),
                )

                item.setText(
                    3,
                    self._format_size(
                        entry.compress_size
                    ),
                )

                item.setData(
                    0,
                    Qt.UserRole,
                    entry.filename,
                )

        self.tree.expandToDepth(
            0
        )

    def _find_entry(self, filename):
        if self.archive is None:
            return None

        for entry in self.entries:
            if entry.filename == filename:
                return entry

        return None

    def _selection_changed(self):
        items = self.tree.selectedItems()

        if not items:
            return

        item = items[0]

        filename = item.data(
            0,
            Qt.UserRole,
        )

        if not filename:
            self._show_text(
                "フォルダ\n\n"
                f"{item.text(0)}"
            )

            return

        entry = self._find_entry(
            filename
        )

        if entry is None:
            return

        if entry.is_dir():
            return

        self._preview_entry(
            entry
        )

    def _preview_entry(self, entry):
        suffix = Path(
            entry.filename
        ).suffix.lower()

        if suffix in self.IMAGE_EXTENSIONS:
            self._show_image(
                entry
            )
            return

        if suffix in self.TEXT_EXTENSIONS:
            self._show_text_file(
                entry
            )
            return

        self.preview_image.hide()
        self.preview.show()

        compression = (
            "保存"
            if entry.compress_type
            == zipfile.ZIP_STORED
            else "圧縮"
        )

        text = (
            f"ファイル名: {entry.filename}\n\n"
            f"種類: {self._file_type(entry)}\n"
            f"サイズ: {self._format_size(entry.file_size)}\n"
            f"圧縮後: "
            f"{self._format_size(entry.compress_size)}\n"
            f"方式: {compression}\n"
            f"CRC32: "
            f"{entry.CRC:08X}\n"
            f"更新日時: "
            f"{entry.date_time[0]:04d}/"
            f"{entry.date_time[1]:02d}/"
            f"{entry.date_time[2]:02d} "
            f"{entry.date_time[3]:02d}:"
            f"{entry.date_time[4]:02d}:"
            f"{entry.date_time[5]:02d}\n"
        )

        self._show_text(
            text
        )

    def _show_text_file(self, entry):
        try:
            data = self.archive.read(
                entry
            )

            text = data.decode(
                "utf-8"
            )

        except UnicodeDecodeError:
            try:
                text = data.decode(
                    "shift_jis"
                )
            except UnicodeDecodeError:
                self._show_text(
                    "このファイルはテキストとして"
                    "表示できません。\n\n"
                    f"{entry.filename}"
                )
                return

        except Exception as exc:
            self._show_text(
                "ファイルを読み込めませんでした。\n\n"
                f"{exc}"
            )
            return

        self._show_text(
            text
        )

    def _show_image(self, entry):
        try:
            data = self.archive.read(
                entry
            )

            pixmap = QPixmap()

            if not pixmap.loadFromData(
                data
            ):
                raise ValueError(
                    "画像として読み込めません。"
                )

            self.preview.hide()
            self.preview_image.show()

            self.preview_image.setPixmap(
                pixmap
            )

            self.preview_image.setScaledContents(
                False
            )

        except Exception as exc:
            self._show_text(
                "画像を表示できませんでした。\n\n"
                f"{exc}"
            )

    def _show_text(self, text):
        self.preview_image.hide()
        self.preview.show()

        self.preview.setPlainText(
            text
        )

    def _extract_all(self):
        if self.archive is None:
            return

        directory = QFileDialog.getExistingDirectory(
            self,
            "展開先を選択",
        )

        if not directory:
            return

        try:
            self.archive.extractall(
                directory
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "open",
                "展開に失敗しました。\n\n"
                f"{exc}",
            )
            return

        QMessageBox.information(
            self,
            "open",
            "ZIPファイルを展開しました。",
        )

    def _extract_selected(self):
        if self.archive is None:
            return

        items = self.tree.selectedItems()

        if not items:
            QMessageBox.information(
                self,
                "open",
                "展開するファイルを選択してください。",
            )
            return

        item = items[0]

        filename = item.data(
            0,
            Qt.UserRole,
        )

        if not filename:
            QMessageBox.information(
                self,
                "open",
                "ファイルを選択してください。",
            )
            return

        entry = self._find_entry(
            filename
        )

        if entry is None or entry.is_dir():
            return

        directory = QFileDialog.getExistingDirectory(
            self,
            "展開先を選択",
        )

        if not directory:
            return

        try:
            target = Path(
                directory
            )

            target_path = (
                target
                / Path(filename)
            )

            target_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with self.archive.open(
                entry,
                "r",
            ) as source:
                target_path.write_bytes(
                    source.read()
                )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "open",
                "ファイルの展開に失敗しました。\n\n"
                f"{exc}",
            )
            return

        QMessageBox.information(
            self,
            "open",
            "ファイルを展開しました。",
        )

    def _refresh(self):
        self.tree.clear()
        self.preview.clear()

        if self.archive is not None:
            try:
                self.archive.close()
            except Exception:
                pass

            self.archive = None

        self._open_archive()

    @staticmethod
    def _file_type(entry):
        suffix = Path(
            entry.filename
        ).suffix.lower()

        if suffix:
            mime_type, _ = mimetypes.guess_type(
                entry.filename
            )

            if mime_type:
                return mime_type

            return suffix

        return "不明"

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
        if self.archive is not None:
            try:
                self.archive.close()
            except Exception:
                pass

            self.archive = None

        super().closeEvent(
            event
        )