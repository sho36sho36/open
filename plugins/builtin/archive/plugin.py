from core.plugin import FilePlugin

from .archive_viewer import ArchiveViewer


class ArchivePlugin(FilePlugin):
    """圧縮・アーカイブファイルを表示するプラグイン。"""

    name = "Archive Plugin"
    version = "2.0.1"

    description = (
        "ZIP / 7Z / TAR / GZ / BZ2 / XZ / RAR / CAB "
        "などの圧縮・アーカイブファイルを表示します。"
    )

    extensions = [
        ".zip",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".rar",
        ".cab",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return ArchiveViewer(
            file_info,
            parent=parent,
        )