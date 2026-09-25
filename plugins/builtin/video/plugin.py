from core.plugin import FilePlugin

from plugins.builtin.video.video_viewer import VideoViewer


class VideoPlugin(FilePlugin):
    """一般的な動画ファイルに対応する共通プラグイン。"""

    name = "Video Plugin"
    version = "1.3.0"

    description = (
        "一般的な動画ファイルを再生する"
        "共通ビデオプラグインです。"
    )

    extensions = [
        ".mp4",
        ".mkv",
        ".webm",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".mpeg",
        ".mpg",
        ".m4v",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return VideoViewer(
            file_info,
            parent,
        )