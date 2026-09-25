from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class BaseViewer(QWidget):
    """すべてのViewerの基本クラス。"""

    def __init__(self, file_info, parent=None):
        super().__init__(parent)

        self.file_info = file_info

        self.layout = QVBoxLayout(self)

    def clear_view(self):
        """表示内容をクリアします。"""

        while self.layout.count():
            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()


class UnsupportedViewer(BaseViewer):
    """対応プラグインが存在しない場合の表示。"""

    def __init__(self, file_info, parent=None):
        super().__init__(file_info, parent)

        label = QLabel(
            f"このファイル形式には対応していません。\n\n"
            f"ファイル: {file_info.name}\n"
            f"拡張子: {file_info.extension or 'なし'}"
        )

        label.setWordWrap(True)
        label.setStyleSheet(
            "font-size: 16px; padding: 30px;"
        )

        self.layout.addWidget(label)