from pathlib import Path


class FileInfo:
    """開こうとしているファイルの情報を保持します。"""

    def __init__(self, path):
        self.path = Path(path)

    @property
    def name(self):
        return self.path.name

    @property
    def extension(self):
        return self.path.suffix.lower()

    @property
    def exists(self):
        return self.path.exists()

    @property
    def is_file(self):
        return self.path.is_file()

    @property
    def size(self):
        if not self.exists or not self.is_file:
            return 0

        try:
            return self.path.stat().st_size
        except OSError:
            return 0

    def __repr__(self):
        return f"FileInfo({str(self.path)!r})"