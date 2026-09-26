import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .plugin_manager import PluginManager
from .file_detector import FileDetector
from .file_info import FileInfo


class FileFusionApplication:
    """openアプリケーション本体。"""

    VERSION = "1.4.0"

    def __init__(self):
        self.qt_app = QApplication(sys.argv)

        self.qt_app.setApplicationName("open")
        self.qt_app.setApplicationDisplayName("open")
        self.qt_app.setApplicationVersion(
            self.VERSION
        )

        self.detector = FileDetector()

        base_directory = (
            Path(__file__).resolve().parent.parent
        )

        builtin_directory = (
            base_directory
            / "plugins"
            / "builtin"
        )

        external_directory = (
            base_directory
            / "plugins"
            / "external"
        )

        self.plugin_manager = PluginManager(
            [
                builtin_directory,
                external_directory,
            ]
        )

        self.plugin_manager.discover()
        self.plugin_manager.initialize_all()

        from ui.main_window import MainWindow

        self.window = MainWindow(self)

    def open_file(self, path):
        """ファイルをopenで開きます。"""

        file_info = FileInfo(path)

        self.window.show_file(
            file_info
        )

    def run(self):
        self.window.show()

        exit_code = self.qt_app.exec()

        self.plugin_manager.shutdown_all()

        sys.exit(exit_code)