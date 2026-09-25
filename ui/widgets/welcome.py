from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class WelcomeWidget(QLabel):
    """初期画面。"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setText(
            "Open\n\n"
            "ファイルを開いてください。"
        )

        self.setAlignment(Qt.AlignCenter)

        self.setStyleSheet(
            "font-size: 20px; padding: 40px;"
        )