import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .plugin_manager import PluginManager
from .file_detector import FileDetector
from .file_info import FileInfo
from .logger import get_logger


class FileFusionApplication:
    """openアプリケーション本体。"""

    VERSION = "3.0.0"

    def __init__(self):
        self.logger = get_logger(
            "application"
        )

        self.logger.info(
            "open v%s を起動します。",
            self.VERSION,
        )

        self.qt_app = QApplication(
            sys.argv
        )

        self.qt_app.setApplicationName(
            "open"
        )

        self.qt_app.setApplicationDisplayName(
            "open"
        )

        self.qt_app.setApplicationVersion(
            self.VERSION
        )

        self.detector = FileDetector()

        base_directory = (
            Path(__file__)
            .resolve()
            .parent
            .parent
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

        try:
            self.plugin_manager.discover()

            self.plugin_manager.initialize_all()

            self.logger.info(
                "%d個のPluginを読み込みました。",
                len(
                    self.plugin_manager.all_plugins()
                ),
            )

        except Exception as exc:
            self.logger.exception(
                "Pluginの初期化中にエラーが発生しました。"
            )

            # Pluginの一部に問題があっても
            # open本体は起動できるようにします。
            try:
                self.plugin_manager.shutdown_all()
            except Exception:
                self.logger.exception(
                    "Plugin終了処理中にエラーが発生しました。"
                )

        from ui.main_window import MainWindow

        self.window = MainWindow(
            self
        )

        self.logger.info(
            "メインウィンドウを作成しました。"
        )

    def open_file(self, path):
        """ファイルをopenで開きます。"""

        try:
            file_info = FileInfo(
                path
            )

            self.window.show_file(
                file_info
            )

        except Exception:
            self.logger.exception(
                "Applicationからファイルを開けませんでした: %s",
                path,
            )

    def run(self):
        """アプリケーションを開始します。"""

        self.window.show()

        self.logger.info(
            "GUIを開始しました。"
        )

        exit_code = self.qt_app.exec()

        self.logger.info(
            "GUIが終了しました。"
        )

        try:
            self.plugin_manager.shutdown_all()

        except Exception:
            self.logger.exception(
                "Plugin終了処理中にエラーが発生しました。"
            )

        self.logger.info(
            "openを終了します。"
        )

        sys.exit(
            exit_code
        )