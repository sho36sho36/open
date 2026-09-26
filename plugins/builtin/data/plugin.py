from .data_viewer import DataViewer

from core.plugin import FilePlugin


class DataPlugin(FilePlugin):
    """データファイルを表示するプラグイン。"""

    name = "Data Plugin"
    version = "2.0.2"
    description = (
        "SQLite、Parquet、JSONL、NDJSON "
        "などのデータファイルを表示します。"
    )

    extensions = [
        ".db",
        ".sqlite",
        ".sqlite3",
        ".parquet",
        ".jsonl",
        ".ndjson",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return DataViewer(
            file_info,
            parent,
        )