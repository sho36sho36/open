from core.plugin import FilePlugin

from .design_viewer import DesignViewer


class DesignPlugin(FilePlugin):
    """デザイン・ベクターファイルを表示するプラグイン。"""

    name = "Design / Vector Plugin"
    version = "2.2.0"

    description = (
        "SVG、EPS、AI、PSD、XCF、KRAなどの"
        "デザインファイルを表示します。"
    )

    extensions = [
        ".svg",
        ".eps",
        ".ai",
        ".psd",
        ".xcf",
        ".kra",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return DesignViewer(
            file_info,
            parent,
        )