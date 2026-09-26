from core.plugin import FilePlugin

from plugins.builtin.pdf.pdf_viewer import PDFViewer


class PDFPlugin(FilePlugin):
    """PDFファイルに対応する共通プラグイン。"""

    name = "PDF Plugin"
    version = "1.5.0"

    description = (
        "PDFファイルを表示する"
        "共通PDFプラグインです。"
    )

    extensions = [
        ".pdf",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return PDFViewer(
            file_info,
            parent,
        )