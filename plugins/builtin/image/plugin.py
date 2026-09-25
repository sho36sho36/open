from core.plugin import FilePlugin

from plugins.builtin.image.image_viewer import ImageViewer


class ImagePlugin(FilePlugin):
    """一般的な画像ファイルに対応する共通プラグイン。"""

    name = "Image Plugin"
    version = "1.1.1"

    description = (
        "一般的な画像ファイルを表示する"
        "共通イメージプラグインです。"
    )

    extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".webp",
        ".tiff",
        ".tif",
        ".ico",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return ImageViewer(
            file_info,
            parent,
        )