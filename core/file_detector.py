from pathlib import Path

from .file_info import FileInfo


class FileDetector:
    """ファイル情報を検出します。"""

    def detect(self, path):
        """指定されたファイルの情報を取得します。"""

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"ファイルが存在しません: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"ファイルではありません: {path}"
            )

        return FileInfo(path)