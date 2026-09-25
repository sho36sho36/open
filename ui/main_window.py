from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QFrame,
)

from core.viewer import UnsupportedViewer


class MainWindow(QMainWindow):
    """FileFusionのメインウィンドウ。"""

    def __init__(self, application):
        super().__init__()

        self.application = application
        self.current_viewer = None

        self.setWindowTitle("FileFusion 1.0.0")
        self.resize(1000, 700)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        toolbar = QFrame()
        toolbar.setFrameShape(QFrame.StyledPanel)

        toolbar_layout = QHBoxLayout(toolbar)

        open_button = QPushButton("📂 開く")
        open_button.clicked.connect(self.open_dialog)

        plugins_button = QPushButton("🔌 プラグイン")
        plugins_button.clicked.connect(self.show_plugins)

        toolbar_layout.addWidget(open_button)
        toolbar_layout.addWidget(plugins_button)
        toolbar_layout.addStretch()

        self.status_label = QLabel("FileFusion v1.0.0")

        toolbar_layout.addWidget(self.status_label)

        root.addWidget(toolbar)

        self.viewer_container = QWidget()
        self.viewer_layout = QVBoxLayout(
            self.viewer_container
        )

        self.viewer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.addWidget(
            self.viewer_container,
            1,
        )

        self.show_welcome()

    def show_welcome(self):
        self._clear_viewer()

        label = QLabel(
            "Open\n\n"
            "ファイルを開いてください。\n\n"
            "プラグイン方式で、さまざまな形式に対応できます。"
        )

        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet(
            "font-size: 20px; padding: 40px;"
        )

        self.viewer_layout.addWidget(label)

    def _clear_viewer(self):
        if self.current_viewer is not None:
            self.current_viewer.deleteLater()
            self.current_viewer = None

        while self.viewer_layout.count():
            item = self.viewer_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "ファイルを開く",
            "",
            "すべてのファイル (*.*)",
        )

        if path:
            self.application.open_file(path)

    def show_file(self, file_info):
        self._clear_viewer()

        if not file_info.exists:
            self.status_label.setText(
                "ファイルが存在しません"
            )

            self.show_welcome()
            return

        plugin = self.application.plugin_manager.find_plugin(
            file_info
        )

        if plugin is None:
            viewer = UnsupportedViewer(
                file_info,
                self.viewer_container,
            )

            self.current_viewer = viewer

            self.viewer_layout.addWidget(viewer)

            self.status_label.setText(
                f"未対応: {file_info.name}"
            )

            return

        try:
            viewer = plugin.create_viewer(
                file_info,
                self.viewer_container,
            )

            if viewer is None:
                raise RuntimeError(
                    "プラグインがViewerを返しませんでした。"
                )

            self.current_viewer = viewer

            self.viewer_layout.addWidget(viewer)

            self.status_label.setText(
                f"{plugin.name} | {file_info.name}"
            )

        except Exception as exc:
            label = QLabel(
                "ファイルを開けませんでした。\n\n"
                f"{exc}"
            )

            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)

            self.current_viewer = label

            self.viewer_layout.addWidget(label)

            self.status_label.setText(
                "読み込みエラー"
            )

    def show_plugins(self):
        self._clear_viewer()

        plugins = (
            self.application
            .plugin_manager
            .all_plugins()
        )

        layout = QVBoxLayout()

        title = QLabel("🔌 インストール済みプラグイン")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        layout.addWidget(title)

        for plugin in plugins:
            extensions = ", ".join(
                plugin.extensions
            )

            label = QLabel(
                f"{plugin.name}  v{plugin.version}\n"
                f"{plugin.description}\n"
                f"対応: {extensions}"
            )

            label.setWordWrap(True)

            label.setStyleSheet(
                "padding: 15px;"
                "border-bottom: 1px solid #cccccc;"
            )

            layout.addWidget(label)

        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.current_viewer = container

        self.viewer_layout.addWidget(container)

        self.status_label.setText(
            f"プラグイン数: {len(plugins)}"
        )