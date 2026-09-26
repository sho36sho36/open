from pathlib import Path
import logging
import traceback

from PySide6.QtCore import (
    Qt,
    QDir,
    Signal,
)
from PySide6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QFileSystemModel,
    QTabWidget,
    QSplitter,
    QMainWindow,
)

from core.viewer import UnsupportedViewer


# ==============================================================
# ログ設定
# ==============================================================

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
LOG_DIRECTORY = BASE_DIRECTORY / "logs"
LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIRECTORY / "open.log"

logger = logging.getLogger("open")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s "
        "[%(levelname)s] "
        "%(name)s: "
        "%(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )


# ==============================================================
# File Browser
# ==============================================================


class FileBrowser(QWidget):
    """
    open用ファイルブラウザ。

    機能:
    - フォルダ表示
    - ファイル表示
    - ダブルクリックで開く
    - フォルダ移動
    - 再読み込み
    - 再帰検索
    """

    file_open_requested = Signal(Path)

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        self.current_root = Path.cwd()

        self._build_ui()
        self._setup_model()
        self._connect_signals()

        self.set_root(
            self.current_root
        )

    def _build_ui(self):
        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        layout.setSpacing(6)

        title = QLabel(
            "📁 ファイルブラウザ"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 4px;
            }
            """
        )

        layout.addWidget(title)

        path_layout = QHBoxLayout()

        self.path_edit = QLineEdit()

        self.path_edit.setPlaceholderText(
            "フォルダのパス"
        )

        path_layout.addWidget(
            self.path_edit,
            1,
        )

        self.go_button = QPushButton(
            "移動"
        )

        path_layout.addWidget(
            self.go_button
        )

        layout.addLayout(
            path_layout
        )

        button_layout = QHBoxLayout()

        self.folder_button = QPushButton(
            "📂 フォルダ"
        )

        self.refresh_button = QPushButton(
            "🔄 更新"
        )

        button_layout.addWidget(
            self.folder_button
        )

        button_layout.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            button_layout
        )

        search_layout = QHBoxLayout()

        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "🔎 ファイル名を検索..."
        )

        search_layout.addWidget(
            self.search_edit,
            1,
        )

        self.search_button = QPushButton(
            "検索"
        )

        search_layout.addWidget(
            self.search_button
        )

        layout.addLayout(
            search_layout
        )

        self.model = QFileSystemModel(
            self
        )

        self.model.setFilter(
            QDir.Filter.AllEntries
            | QDir.Filter.NoDotAndDotDot
        )

        self.tree = QTreeView(
            self
        )

        self.tree.setModel(
            self.model
        )

        self.tree.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tree.setAlternatingRowColors(
            True
        )

        self.tree.setColumnWidth(
            0,
            220,
        )

        layout.addWidget(
            self.tree,
            1,
        )

        self.search_label = QLabel(
            "検索結果"
        )

        self.search_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.search_label.hide()

        layout.addWidget(
            self.search_label
        )

        self.search_results = QListWidget(
            self
        )

        self.search_results.hide()

        self.search_results.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        layout.addWidget(
            self.search_results,
            1,
        )

    def _setup_model(self):
        self.model.setRootPath(
            str(self.current_root)
        )

    def _connect_signals(self):
        self.go_button.clicked.connect(
            self.go_to_path
        )

        self.path_edit.returnPressed.connect(
            self.go_to_path
        )

        self.folder_button.clicked.connect(
            self.choose_folder
        )

        self.refresh_button.clicked.connect(
            self.refresh
        )

        self.search_button.clicked.connect(
            self.search_files
        )

        self.search_edit.returnPressed.connect(
            self.search_files
        )

        self.tree.doubleClicked.connect(
            self._tree_double_clicked
        )

        self.search_results.itemDoubleClicked.connect(
            self._search_result_double_clicked
        )

    def set_root(
        self,
        path,
    ):
        path = Path(path).expanduser()

        try:
            path = path.resolve()
        except OSError:
            pass

        if not path.exists():
            QMessageBox.warning(
                self,
                "フォルダがありません",
                f"フォルダが見つかりません。\n\n{path}",
            )
            return

        if not path.is_dir():
            QMessageBox.warning(
                self,
                "フォルダではありません",
                f"指定されたパスはフォルダではありません。\n\n{path}",
            )
            return

        self.current_root = path

        self.path_edit.setText(
            str(path)
        )

        index = self.model.index(
            str(path)
        )

        if index.isValid():
            self.tree.setRootIndex(
                index
            )

        self.search_results.clear()
        self.search_results.hide()

        self.search_label.hide()

        self.tree.show()

        logger.info(
            "ファイルブラウザ移動: %s",
            path,
        )

    def go_to_path(self):
        text = self.path_edit.text().strip()

        if not text:
            return

        self.set_root(
            Path(text)
        )

    def choose_folder(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "フォルダを選択",
            str(self.current_root),
        )

        if not path:
            return

        self.set_root(
            Path(path)
        )

    def refresh(self):
        current = self.current_root

        self.model.setRootPath(
            str(current)
        )

        index = self.model.index(
            str(current)
        )

        if index.isValid():
            self.tree.setRootIndex(
                index
            )

        self.search_results.clear()

        logger.info(
            "ファイルブラウザ更新: %s",
            current,
        )

    def _tree_double_clicked(
        self,
        index,
    ):
        if not index.isValid():
            return

        path = Path(
            self.model.filePath(
                index
            )
        )

        if path.is_file():
            self.file_open_requested.emit(
                path
            )

    def search_files(self):
        query = (
            self.search_edit
            .text()
            .strip()
            .lower()
        )

        if not query:
            self.search_results.clear()
            self.search_results.hide()
            self.search_label.hide()
            self.tree.show()
            return

        self.search_results.clear()

        self.tree.hide()

        self.search_label.setText(
            f"🔎 検索中: {query}"
        )

        self.search_label.show()
        self.search_results.show()

        count = 0

        try:
            for path in self._iter_files(
                self.current_root
            ):
                if query in path.name.lower():
                    item = QListWidgetItem(
                        path.name
                    )

                    item.setToolTip(
                        str(path)
                    )

                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        str(path),
                    )

                    self.search_results.addItem(
                        item
                    )

                    count += 1

                    if count >= 5000:
                        break

        except Exception as exc:
            logger.exception(
                "ファイル検索エラー"
            )

            QMessageBox.warning(
                self,
                "検索エラー",
                "ファイル検索中にエラーが発生しました。\n\n"
                f"{type(exc).__name__}: {exc}",
            )

            return

        self.search_label.setText(
            f"🔎 検索結果: {count}件"
        )

        logger.info(
            "ファイル検索: query=%r results=%d root=%s",
            query,
            count,
            self.current_root,
        )

    def _iter_files(
        self,
        root,
    ):
        root = Path(root)

        try:
            entries = list(
                root.iterdir()
            )

        except (
            PermissionError,
            OSError,
        ):
            return

        for entry in entries:
            try:
                if entry.is_file():
                    yield entry

                elif entry.is_dir():
                    yield from self._iter_files(
                        entry
                    )

            except (
                PermissionError,
                OSError,
            ):
                continue

    def _search_result_double_clicked(
        self,
        item,
    ):
        if item is None:
            return

        path_text = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not path_text:
            return

        path = Path(
            path_text
        )

        if path.exists() and path.is_file():
            self.file_open_requested.emit(
                path
            )

    def show_current_directory(self):
        self.search_edit.clear()

        self.search_results.clear()
        self.search_results.hide()

        self.search_label.hide()

        self.tree.show()

    def open_parent_directory(self):
        parent = self.current_root.parent

        if parent == self.current_root:
            return

        self.set_root(
            parent
        )


# ==============================================================
# Main Window
# ==============================================================


class MainWindow(QMainWindow):
    """
    open v3.0.0 メインウィンドウ。

    v3.0.0:
    - タブ
    - ドラッグ＆ドロップ
    - ファイルブラウザ
    - 検索
    - エラーログ
    """

    def __init__(
        self,
        application,
        parent=None,
    ):
        super().__init__(parent)

        self.application = application

        self.plugin_manager = (
            application.plugin_manager
        )

        self.file_detector = (
            application.detector
        )

        self.current_viewer = None
        self.current_file = None

        self.setWindowTitle(
            "open"
        )

        self.resize(
            1400,
            900,
        )

        self.setAcceptDrops(
            True
        )

        self._build_ui()

        logger.info(
            "open v3.0.0 起動"
        )

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self):
        central_widget = QWidget(
            self
        )

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            6,
            6,
            6,
            6,
        )

        # ------------------------------------------------------
        # Toolbar
        # ------------------------------------------------------

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

        self.browser_button = QPushButton(
            "📁 ファイルブラウザ"
        )

        self.browser_button.clicked.connect(
            self.toggle_browser
        )

        toolbar.addWidget(
            self.browser_button
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

        self.log_button = QPushButton(
            "🧾 エラーログ"
        )

        self.log_button.clicked.connect(
            self.show_error_log
        )

        toolbar.addWidget(
            self.log_button
        )

        toolbar.addStretch()

        self.file_label = QLabel(
            "ファイルが開かれていません"
        )

        self.file_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        toolbar.addWidget(
            self.file_label
        )

        main_layout.addLayout(
            toolbar
        )

        # ------------------------------------------------------
        # Browser + Viewer
        # ------------------------------------------------------

        self.browser = FileBrowser(
            self
        )

        self.browser.file_open_requested.connect(
            self.open_file
        )

        self.browser.setMinimumWidth(
            260
        )

        self.browser.setMaximumWidth(
            450
        )

        self.browser.hide()

        # ------------------------------------------------------
        # Tabs
        # ------------------------------------------------------

        self.tab_widget = QTabWidget(
            self
        )

        self.tab_widget.setTabsClosable(
            True
        )

        self.tab_widget.setMovable(
            True
        )

        self.tab_widget.tabCloseRequested.connect(
            self.close_tab
        )

        self.tab_widget.currentChanged.connect(
            self.current_tab_changed
        )

        # ホーム
        self.home_widget = (
            self._create_home_widget()
        )

        self.tab_widget.addTab(
            self.home_widget,
            "🏠 ホーム",
        )

        self.tab_widget.setCurrentWidget(
            self.home_widget
        )

        # ------------------------------------------------------
        # Splitter
        # ------------------------------------------------------

        self.splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.splitter.addWidget(
            self.browser
        )

        self.splitter.addWidget(
            self.tab_widget
        )

        self.splitter.setStretchFactor(
            0,
            0,
        )

        self.splitter.setStretchFactor(
            1,
            1,
        )

        main_layout.addWidget(
            self.splitter,
            1,
        )

    def _create_home_widget(self):
        widget = QWidget()

        layout = QVBoxLayout(
            widget
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel(
            "📂 open"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size: 36px;
            font-weight: bold;
            """
        )

        layout.addWidget(
            title
        )

        description = QLabel(
            "いろいろなファイルを\n"
            "プラグインで開けるファイルビューア"
        )

        description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        description.setStyleSheet(
            """
            font-size: 17px;
            margin-top: 10px;
            """
        )

        layout.addWidget(
            description
        )

        open_button = QPushButton(
            "📂 ファイルを開く"
        )

        open_button.setMinimumSize(
            240,
            48,
        )

        open_button.clicked.connect(
            self.open_file_dialog
        )

        layout.addWidget(
            open_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        drop_label = QLabel(
            "または、ここへファイルをドラッグ＆ドロップ"
        )

        drop_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        drop_label.setStyleSheet(
            """
            color: #777;
            margin-top: 20px;
            """
        )

        layout.addWidget(
            drop_label
        )

        return widget

    # ==========================================================
    # File dialog
    # ==========================================================

    def open_file_dialog(self):
        path_list, _ = (
            QFileDialog.getOpenFileNames(
                self,
                "ファイルを開く",
                "",
                "すべてのファイル (*.*)",
            )
        )

        if not path_list:
            return

        for path in path_list:
            self.open_file(
                Path(path)
            )

    # ==========================================================
    # File opening
    # ==========================================================

    def open_file(
        self,
        path,
    ):
        path = Path(path)

        try:
            path = path.expanduser().resolve()
        except OSError:
            pass

        if not path.exists():
            self._show_error(
                "ファイルがありません",
                f"ファイルが見つかりません。\n\n{path}",
            )
            return

        if not path.is_file():
            self._show_error(
                "ファイルではありません",
                f"指定されたパスはファイルではありません。\n\n{path}",
            )
            return

        # すでに開いているファイルなら、そのタブへ移動
        existing_index = self._find_file_tab(
            path
        )

        if existing_index >= 0:
            self.tab_widget.setCurrentIndex(
                existing_index
            )

            logger.info(
                "既存タブを選択: %s",
                path,
            )

            return

        logger.info(
            "ファイルを開く: %s",
            path,
        )

        # ------------------------------------------------------
        # FileInfo
        # ------------------------------------------------------

        try:
            file_info = (
                self.file_detector.detect(
                    path
                )
            )

        except Exception as exc:
            logger.exception(
                "FileInfo作成エラー: %s",
                path,
            )

            self._show_error(
                "ファイル検出エラー",
                "ファイル情報を取得できませんでした。\n\n"
                f"{type(exc).__name__}: {exc}",
            )

            return

        # ------------------------------------------------------
        # Plugin
        # ------------------------------------------------------

        plugin = (
            self.plugin_manager.find_plugin(
                file_info
            )
        )

        # ------------------------------------------------------
        # Viewer
        # ------------------------------------------------------

        if plugin is None:
            viewer = UnsupportedViewer(
                file_info,
                self,
            )

            plugin_name = "未対応"

        else:
            plugin_name = plugin.name

            try:
                viewer = (
                    plugin.create_viewer(
                        file_info,
                        self,
                    )
                )

                if viewer is None:
                    raise RuntimeError(
                        "プラグインがViewerを返しませんでした。"
                    )

            except Exception as exc:
                logger.exception(
                    "Viewer作成エラー: plugin=%s file=%s",
                    plugin.name,
                    path,
                )

                self._show_error(
                    "ファイルを開けません",
                    "プラグインによるファイルの表示に失敗しました。\n\n"
                    f"プラグイン: {plugin.name}\n"
                    f"ファイル: {file_info.name}\n\n"
                    f"{type(exc).__name__}: {exc}\n\n"
                    f"詳細は {LOG_FILE} を確認してください。",
                )

                return

        # ------------------------------------------------------
        # Tab
        # ------------------------------------------------------

        viewer.setProperty(
            "open_file_path",
            str(path),
        )

        viewer.setProperty(
            "open_plugin_name",
            plugin_name,
        )

        index = self.tab_widget.addTab(
            viewer,
            self._tab_title(path),
        )

        self.tab_widget.setCurrentIndex(
            index
        )

        self.current_viewer = viewer
        self.current_file = path

        self.file_label.setText(
            f"📄 {path.name}"
        )

        self.setWindowTitle(
            f"open - {path.name}"
        )

        logger.info(
            "ファイルを開きました: plugin=%s file=%s",
            plugin_name,
            path,
        )

    def show_file(
        self,
        file_info,
    ):
        self.open_file(
            file_info.path
        )

    # ==========================================================
    # Tabs
    # ==========================================================

    @staticmethod
    def _tab_title(
        path,
    ):
        return f"📄 {Path(path).name}"

    def _find_file_tab(
        self,
        path,
    ):
        path = Path(path)

        try:
            target = path.resolve()
        except OSError:
            target = path

        for index in range(
            self.tab_widget.count()
        ):
            widget = self.tab_widget.widget(
                index
            )

            if widget is None:
                continue

            file_path = widget.property(
                "open_file_path"
            )

            if not file_path:
                continue

            try:
                opened = Path(
                    file_path
                ).resolve()
            except OSError:
                opened = Path(
                    file_path
                )

            if opened == target:
                return index

        return -1

    def close_tab(
        self,
        index,
    ):
        if index < 0:
            return

        widget = self.tab_widget.widget(
            index
        )

        if widget is self.home_widget:
            return

        file_path = widget.property(
            "open_file_path"
        )

        try:
            widget.close()
        except Exception:
            logger.exception(
                "Viewer終了エラー"
            )

        self.tab_widget.removeTab(
            index
        )

        widget.deleteLater()

        logger.info(
            "タブを閉じました: %s",
            file_path or "unknown",
        )

        if self.tab_widget.count() == 0:
            home_index = self.tab_widget.addTab(
                self.home_widget,
                "🏠 ホーム",
            )

            self.tab_widget.setCurrentIndex(
                home_index
            )

        self._update_current_file()

    def current_tab_changed(
        self,
        index,
    ):
        if index < 0:
            return

        widget = self.tab_widget.widget(
            index
        )

        if widget is None:
            return

        if widget is self.home_widget:
            self.current_viewer = None
            self.current_file = None

            self.file_label.setText(
                "ファイルが開かれていません"
            )

            self.setWindowTitle(
                "open"
            )

            return

        self.current_viewer = widget

        file_path = widget.property(
            "open_file_path"
        )

        if file_path:
            self.current_file = Path(
                file_path
            )

            self.file_label.setText(
                f"📄 {self.current_file.name}"
            )

            self.setWindowTitle(
                f"open - {self.current_file.name}"
            )

    def _update_current_file(self):
        index = self.tab_widget.currentIndex()

        self.current_tab_changed(
            index
        )

    # ==========================================================
    # Browser
    # ==========================================================

    def toggle_browser(self):
        if self.browser.isVisible():
            self.browser.hide()

            self.browser_button.setText(
                "📁 ファイルブラウザ"
            )

        else:
            self.browser.show()

            self.browser_button.setText(
                "📁 ブラウザを閉じる"
            )

    # ==========================================================
    # Drag & Drop
    # ==========================================================

    def dragEnterEvent(
        self,
        event: QDragEnterEvent,
    ):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    event.acceptProposedAction()
                    return

        event.ignore()

    def dropEvent(
        self,
        event: QDropEvent,
    ):
        paths = []

        for url in event.mimeData().urls():
            if not url.isLocalFile():
                continue

            path = Path(
                url.toLocalFile()
            )

            if path.is_file():
                paths.append(
                    path
                )

        if not paths:
            event.ignore()
            return

        event.acceptProposedAction()

        logger.info(
            "ドラッグ＆ドロップ: %d件",
            len(paths),
        )

        for path in paths:
            self.open_file(
                path
            )

    # ==========================================================
    # Plugins
    # ==========================================================

    def show_plugins(self):
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

    # ==========================================================
    # Error logging
    # ==========================================================

    def _show_error(
        self,
        title,
        message,
    ):
        logger.error(
            "%s: %s",
            title,
            message,
        )

        QMessageBox.critical(
            self,
            title,
            message,
        )

    def show_error_log(self):
        """
        エラーログを表示します。

        Windowsでは標準のメモ帳で開きます。
        """

        try:
            if not LOG_FILE.exists():
                LOG_FILE.touch(
                    encoding="utf-8"
                )

            import os

            os.startfile(
                str(LOG_FILE)
            )

            logger.info(
                "エラーログを開きました: %s",
                LOG_FILE,
            )

        except Exception as exc:
            logger.exception(
                "ログファイルを開けませんでした"
            )

            QMessageBox.warning(
                self,
                "ログを開けません",
                "エラーログを開けませんでした。\n\n"
                f"{LOG_FILE}\n\n"
                f"{type(exc).__name__}: {exc}",
            )

    # ==========================================================
    # Close
    # ==========================================================

    def closeEvent(
        self,
        event,
    ):
        logger.info(
            "open終了"
        )

        for index in range(
            self.tab_widget.count()
        ):
            widget = self.tab_widget.widget(
                index
            )

            if widget is None:
                continue

            try:
                widget.close()
            except Exception:
                logger.exception(
                    "Viewer終了エラー"
                )

        event.accept()