from pathlib import Path

from .file_info import FileInfo


class FileDetector:
    """ファイル形式を判定するための基本クラス。"""

    def detect(self, path):
        path = Path(path)

        return FileInfo(path)

    def get_extension(self, path):
        return Path(path).suffix.lower()

    def is_supported_by(self, file_info, plugin):
        return plugin.can_open(file_info)