from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.viewer import UnsupportedViewer


class MainWindow(QMainWindow):
    """FileFusionのメインウィンドウ。"""

    def __init__(
        self,
        application,
        parent=None,
    ):
        super().__init__(parent)

        # FileFusionApplication本体
        self.application = application

        # Applicationが保持しているPluginManager
        self.plugin_manager = (
            application.plugin_manager
        )

        # Applicationが保持しているFileDetector
        self.file_detector = (
            application.detector
        )

        self.current_viewer = None
        self.current_file = None

        self.setWindowTitle("FileFusion")
        self.resize(1200, 800)

        self._build_ui()

    def _build_ui(self):
        """UIを構築します。"""

        central_widget = QWidget()
        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        # ==========================================================
        # ツールバー
        # ==========================================================

        toolbar = QHBoxLayout()

        self.open_button = QPushButton(
            "📂 ファイルを開く"
        )

        self.open_button.clicked.connect(
            self.open_file_dialog
        )

        toolbar.addWidget(
            self.open_button
        )

        self.plugin_button = QPushButton(
            "🔌 プラグイン"
        )

        self.plugin_button.clicked.connect(
            self.show_plugins
        )

        toolbar.addWidget(
            self.plugin_button
        )

        toolbar.addStretch()

        self.file_label = QLabel(
            "ファイルが開かれていません"
        )

        self.file_label.setAlignment(
            Qt.AlignRight
            | Qt.AlignVCenter
        )

        toolbar.addWidget(
            self.file_label
        )

        main_layout.addLayout(
            toolbar
        )

        # ==========================================================
        # Viewer領域
        # ==========================================================

        self.viewer_stack = QStackedWidget()

        main_layout.addWidget(
            self.viewer_stack,
            1,
        )

        # ==========================================================
        # ホーム画面
        # ==========================================================

        self.home_widget = (
            self._create_home_widget()
        )

        self.viewer_stack.addWidget(
            self.home_widget
        )

        self.viewer_stack.setCurrentWidget(
            self.home_widget
        )

    def _create_home_widget(self):
        """ホーム画面を作成します。"""

        widget = QWidget()

        layout = QVBoxLayout(
            widget
        )

        layout.setAlignment(
            Qt.AlignCenter
        )

        title = QLabel(
            "📂 FileFusion"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            "font-size: 32px;"
            "font-weight: bold;"
        )

        layout.addWidget(
            title
        )

        description = QLabel(
            "いろいろなファイルを"
            "プラグインで開けるアプリです。"
        )

        description.setAlignment(
            Qt.AlignCenter
        )

        description.setStyleSheet(
            "font-size: 16px;"
            "margin-top: 10px;"
        )

        layout.addWidget(
            description
        )

        open_button = QPushButton(
            "📂 ファイルを開く"
        )

        open_button.setMinimumWidth(
            220
        )

        open_button.setMinimumHeight(
            45
        )

        open_button.clicked.connect(
            self.open_file_dialog
        )

        layout.addWidget(
            open_button,
            alignment=Qt.AlignCenter,
        )

        return widget

    def open_file_dialog(self):
        """ファイル選択ダイアログを開きます。"""

        path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "ファイルを開く",
                "",
                "すべてのファイル (*.*)",
            )
        )

        if not path:
            return

        self.open_file(
            Path(path)
        )

    def open_file(self, path):
        """指定されたファイルを開きます。"""

        path = Path(path)

        if not path.exists():
            QMessageBox.warning(
                self,
                "ファイルがありません",
                f"ファイルが見つかりません。\n\n"
                f"{path}",
            )

            return

        if not path.is_file():
            QMessageBox.warning(
                self,
                "ファイルではありません",
                f"指定されたパスはファイルではありません。\n\n"
                f"{path}",
            )

            return

        # ==========================================================
        # FileInfoを作成
        # ==========================================================

        try:
            file_info = (
                self.file_detector.detect(
                    path
                )
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "ファイル検出エラー",
                "ファイル情報を取得できませんでした。\n\n"
                f"{type(exc).__name__}: {exc}",
            )

            return

        # ==========================================================
        # 対応プラグインを探す
        # ==========================================================

        plugin = (
            self.plugin_manager.find_plugin(
                file_info
            )
        )

        # ==========================================================
        # Viewerを作成
        # ==========================================================

        if plugin is None:
            viewer = UnsupportedViewer(
                file_info,
                self,
            )

        else:
            try:
                viewer = (
                    plugin.create_viewer(
                        file_info,
                        self,
                    )
                )

            except Exception as exc:
                QMessageBox.critical(
                    self,
                    "ファイルを開けません",
                    "プラグインによるファイルの表示に失敗しました。\n\n"
                    f"プラグイン: {plugin.name}\n"
                    f"ファイル: {file_info.name}\n\n"
                    f"{type(exc).__name__}: {exc}",
                )

                return

        # ==========================================================
        # ★重要★
        #
        # 以前のViewerを完全に取り外す
        # ==========================================================

        old_viewer = (
            self.current_viewer
        )

        if old_viewer is not None:

            try:
                self.viewer_stack.removeWidget(
                    old_viewer
                )
            except Exception:
                pass

            try:
                old_viewer.close()
            except Exception:
                pass

            old_viewer.deleteLater()

            self.current_viewer = None

        # ==========================================================
        # 新しいViewerを追加
        # ==========================================================

        self.current_viewer = viewer

        self.current_file = path

        self.viewer_stack.addWidget(
            viewer
        )

        # ホーム画面ではなく、
        # 今開いたViewerを表示
        self.viewer_stack.setCurrentWidget(
            viewer
        )

        # ==========================================================
        # ウィンドウ表示を更新
        # ==========================================================

        self.file_label.setText(
            f"📄 {path.name}"
        )

        self.setWindowTitle(
            f"FileFusion - {path.name}"
        )

    def show_file(self, file_info):
        """
        FileFusionApplicationから
        ファイルを開く場合にも対応します。
        """

        self.open_file(
            file_info.path
        )

    def show_plugins(self):
        """インストールされているプラグインを表示します。"""

        plugins = (
            self.plugin_manager.all_plugins()
        )

        if not plugins:
            QMessageBox.information(
                self,
                "プラグイン",
                "プラグインが見つかりません。",
            )

            return

        lines = []

        for plugin in plugins:
            extensions = ", ".join(
                plugin.extensions
            )

            lines.append(
                f"🔌 {plugin.name}"
                f"  v{plugin.version}\n"
                f"   {plugin.description}\n"
                f"   対応: {extensions}"
            )

        QMessageBox.information(
            self,
            "🔌 インストール済みプラグイン",
            "\n\n".join(lines),
        )

    def closeEvent(self, event):
        """ウィンドウ終了時の処理。"""

        if self.current_viewer is not None:

            try:
                self.current_viewer.close()
            except Exception:
                pass

        event.accept()