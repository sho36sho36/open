from core.plugin import FilePlugin

from plugins.builtin.audio.audio_viewer import AudioViewer


class AudioPlugin(FilePlugin):
    """一般的な音声ファイルに対応する共通プラグイン。"""

    name = "Audio Plugin"
    version = "1.1.0"

    description = (
        "一般的な音声ファイルを再生する"
        "共通オーディオプラグインです。"
    )

    extensions = [
        ".wav",
        ".mp3",
        ".m4a",
        ".aac",
        ".flac",
        ".ogg",
        ".aiff",
        ".aif",
        ".au",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return AudioViewer(
            file_info,
            parent,
        )