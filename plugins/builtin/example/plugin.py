from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from core.plugin import FilePlugin
from core.viewer import BaseViewer


class ExampleViewer(BaseViewer):
    """v1.0.0の動作確認用Viewer。"""

    def __init__(self, file_info, parent=None):
        super().__init__(file_info, parent)

        label = QLabel(
            "🎉 FileFusion Plugin System\n\n"
            f"ファイル: {file_info.name}\n"
            f"拡張子: {file_info.extension}\n"
            f"サイズ: {file_info.size:,} bytes\n\n"
            "これはサンプルプラグインです。"
        )

        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "font-size: 18px; padding: 40px;"
        )

        self.layout.addWidget(label)


class ExamplePlugin(FilePlugin):
    """FileFusionプラグインのサンプル。"""

    name = "Example Plugin"
    version = "1.0.0"
    description = (
        "FileFusionのプラグインシステムを"
        "確認するためのサンプルプラグイン"
    )

    extensions = [
        ".example",
    ]

    def create_viewer(self, file_info, parent=None):
        return ExampleViewer(
            file_info,
            parent,
        )