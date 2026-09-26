from core.plugin import FilePlugin

from plugins.builtin.archive.archive_viewer import (
    ArchiveViewer,
)


class ArchivePlugin(FilePlugin):
    """圧縮ファイルに対応する共通プラグイン。"""

    name = "Archive Plugin"
    version = "1.6.0"

    description = (
        "ZIP圧縮ファイルを開き、"
        "内容を表示・展開する共通アーカイブプラグインです。"
    )

    extensions = [
        ".zip",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return ArchiveViewer(
            file_info,
            parent,
        )