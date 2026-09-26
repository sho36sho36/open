import bz2
import gzip
import lzma
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    import py7zr
except ImportError:
    py7zr = None

try:
    import rarfile
except ImportError:
    rarfile = None


class ArchiveViewer(QWidget):
    """圧縮・アーカイブファイル用ビューア。"""

    TEXT_EXTENSIONS = {
        ".txt",
        ".log",
        ".csv",
        ".tsv",
        ".json",
        ".jsonl",
        ".ndjson",
        ".xml",
        ".html",
        ".htm",
        ".css",
        ".js",
        ".ts",
        ".py",
        ".java",
        ".c",
        ".h",
        ".cpp",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".rb",
        ".php",
        ".md",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".cfg",
        ".conf",
        ".bat",
        ".cmd",
        ".ps1",
        ".sh",
    }

    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".webp",
        ".tif",
        ".tiff",
        ".ico",
    }

    def __init__(self, file_info, parent=None):
        super().__init__(parent)

        self.file_info = file_info
        self.archive_path = Path(file_info.path)

        self.setObjectName("ArchiveViewer")

        self._build_ui()
        self._load_archive()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)

        header = QHBoxLayout()

        self.title_label = QLabel(
            f"📦 {self.archive_path.name}"
        )

        self.type_label = QLabel(
            self.archive_path.suffix.lower()
        )

        self.status_label = QLabel(
            "読み込み中..."
        )

        self.reload_button = QPushButton(
            "再読み込み"
        )

        self.extract_button = QPushButton(
            "すべて展開"
        )

        header.addWidget(
            self.title_label
        )

        header.addWidget(
            self.type_label
        )

        header.addStretch()

        header.addWidget(
            self.status_label
        )

        header.addWidget(
            self.reload_button
        )

        header.addWidget(
            self.extract_button
        )

        layout.addLayout(header)

        self.tree = QTreeWidget()

        self.tree.setHeaderLabels(
            [
                "名前",
                "種類",
                "サイズ",
            ]
        )

        self.tree.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tree.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        layout.addWidget(
            self.tree
        )

        self.reload_button.clicked.connect(
            self._reload
        )

        self.extract_button.clicked.connect(
            self._extract_all
        )

    # ---------------------------------------------------------
    # Archive loading
    # ---------------------------------------------------------

    def _load_archive(self):
        self.tree.clear()

        try:
            suffix = self.archive_path.suffix.lower()

            if suffix == ".zip":
                self._load_zip()

            elif suffix == ".7z":
                self._load_7z()

            elif suffix == ".tar":
                self._load_tar()

            elif suffix == ".gz":
                self._load_single_compressed(
                    gzip.open
                )

            elif suffix == ".bz2":
                self._load_single_compressed(
                    bz2.open
                )

            elif suffix == ".xz":
                self._load_single_compressed(
                    lzma.open
                )

            elif suffix == ".rar":
                self._load_rar()

            elif suffix == ".cab":
                self._show_error(
                    "CAB形式は現在の環境では"
                    "直接読み込めません。"
                )

            else:
                self._show_error(
                    "対応していないアーカイブ形式です。"
                )

        except Exception as exc:
            self._show_error(
                f"アーカイブを読み込めませんでした。\n\n"
                f"{exc}"
            )

    # ---------------------------------------------------------
    # ZIP
    # ---------------------------------------------------------

    def _load_zip(self):
        with zipfile.ZipFile(
            self.archive_path,
            "r",
        ) as archive:

            for info in archive.infolist():
                self._add_entry(
                    info.filename,
                    info.file_size,
                    info.is_dir(),
                )

            self.status_label.setText(
                f"{len(archive.infolist())} 件"
            )

    # ---------------------------------------------------------
    # 7Z
    # ---------------------------------------------------------

    def _load_7z(self):
        if py7zr is None:
            self._show_error(
                "7Z形式を開くには py7zr が必要です。\n\n"
                "requirements.txt の依存関係をインストールしてください。"
            )
            return

        with py7zr.SevenZipFile(
            self.archive_path,
            mode="r",
        ) as archive:

            names = archive.getnames()

            for name in names:
                self._add_entry(
                    name,
                    0,
                    name.endswith("/"),
                )

            self.status_label.setText(
                f"{len(names)} 件"
            )

    # ---------------------------------------------------------
    # TAR
    # ---------------------------------------------------------

    def _load_tar(self):
        with tarfile.open(
            self.archive_path,
            mode="r:*",
        ) as archive:

            members = archive.getmembers()

            for member in members:
                self._add_entry(
                    member.name,
                    member.size,
                    member.isdir(),
                )

            self.status_label.setText(
                f"{len(members)} 件"
            )

    # ---------------------------------------------------------
    # GZ / BZ2 / XZ
    # ---------------------------------------------------------

    def _load_single_compressed(
        self,
        opener,
    ):
        size = self.archive_path.stat().st_size

        self._add_entry(
            self.archive_path.stem,
            size,
            False,
        )

        self.status_label.setText(
            "単一ファイル圧縮"
        )

    # ---------------------------------------------------------
    # RAR
    # ---------------------------------------------------------

    def _load_rar(self):
        if rarfile is None:
            self._show_error(
                "RAR形式を開くには rarfile が必要です。\n\n"
                "requirements.txt の依存関係をインストールしてください。"
            )
            return

        with rarfile.RarFile(
            self.archive_path,
            "r",
        ) as archive:

            infos = archive.infolist()

            for info in infos:
                self._add_entry(
                    info.filename,
                    info.file_size,
                    info.isdir(),
                )

            self.status_label.setText(
                f"{len(infos)} 件"
            )

    # ---------------------------------------------------------
    # Tree
    # ---------------------------------------------------------

    def _add_entry(
        self,
        name,
        size,
        is_directory,
    ):
        item = QTreeWidgetItem()

        item.setText(
            0,
            name,
        )

        if is_directory:
            item.setText(
                1,
                "フォルダー",
            )

        else:
            item.setText(
                1,
                self._detect_type(name),
            )

        item.setText(
            2,
            self._format_size(size),
        )

        if is_directory:
            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                "directory",
            )
        else:
            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                "file",
            )

        self.tree.addTopLevelItem(
            item
        )

    # ---------------------------------------------------------
    # Type
    # ---------------------------------------------------------

    def _detect_type(self, name):
        suffix = Path(name).suffix.lower()

        if suffix in self.TEXT_EXTENSIONS:
            return "テキスト"

        if suffix in self.IMAGE_EXTENSIONS:
            return "画像"

        if suffix in {
            ".zip",
            ".7z",
            ".tar",
            ".gz",
            ".bz2",
            ".xz",
            ".rar",
            ".cab",
        }:
            return "アーカイブ"

        return "ファイル"

    # ---------------------------------------------------------
    # Extraction
    # ---------------------------------------------------------

    def _extract_all(self):
        destination = QFileDialog.getExistingDirectory(
            self,
            "展開先を選択",
        )

        if not destination:
            return

        destination = Path(destination)

        try:
            suffix = self.archive_path.suffix.lower()

            if suffix == ".zip":
                self._extract_zip(
                    destination
                )

            elif suffix == ".7z":
                self._extract_7z(
                    destination
                )

            elif suffix == ".tar":
                self._extract_tar(
                    destination
                )

            elif suffix == ".gz":
                self._extract_single(
                    gzip.open,
                    destination,
                )

            elif suffix == ".bz2":
                self._extract_single(
                    bz2.open,
                    destination,
                )

            elif suffix == ".xz":
                self._extract_single(
                    lzma.open,
                    destination,
                )

            elif suffix == ".rar":
                self._extract_rar(
                    destination
                )

            elif suffix == ".cab":
                raise RuntimeError(
                    "CAB形式の展開には対応していません。"
                )

            QMessageBox.information(
                self,
                "展開完了",
                f"展開しました。\n\n{destination}",
            )

        except Exception as exc:
            self._show_error(
                f"展開に失敗しました。\n\n{exc}"
            )

    def _extract_zip(
        self,
        destination,
    ):
        with zipfile.ZipFile(
            self.archive_path,
            "r",
        ) as archive:

            archive.extractall(
                destination
            )

    def _extract_7z(
        self,
        destination,
    ):
        if py7zr is None:
            raise RuntimeError(
                "py7zr がインストールされていません。"
            )

        with py7zr.SevenZipFile(
            self.archive_path,
            mode="r",
        ) as archive:

            archive.extractall(
                path=destination
            )

    def _extract_tar(
        self,
        destination,
    ):
        with tarfile.open(
            self.archive_path,
            mode="r:*",
        ) as archive:

            archive.extractall(
                destination
            )

    def _extract_single(
        self,
        opener,
        destination,
    ):
        output_name = self.archive_path.stem

        output_path = (
            destination
            / output_name
        )

        with opener(
            self.archive_path,
            "rb",
        ) as source:

            with output_path.open(
                "wb"
            ) as target:

                shutil.copyfileobj(
                    source,
                    target,
                )

    def _extract_rar(
        self,
        destination,
    ):
        if rarfile is None:
            raise RuntimeError(
                "rarfile がインストールされていません。"
            )

        with rarfile.RarFile(
            self.archive_path,
            "r",
        ) as archive:

            archive.extractall(
                path=destination
            )

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def _format_size(self, size):
        if size is None:
            return "-"

        try:
            size = int(size)
        except (TypeError, ValueError):
            return "-"

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        value = float(size)

        for unit in units:
            if value < 1024:
                return f"{value:.1f} {unit}"

            value /= 1024

        return f"{value:.1f} PB"

    def _show_error(self, message):
        self.status_label.setText(
            "エラー"
        )

        QMessageBox.warning(
            self,
            "Archive Plugin",
            message,
        )

    def _reload(self):
        self._load_archive()