import json
import sqlite3

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class DataViewer(QWidget):
    """データファイルを表示するViewer。"""

    SQLITE_EXTENSIONS = {
        ".db",
        ".sqlite",
        ".sqlite3",
    }

    PARQUET_EXTENSIONS = {
        ".parquet",
    }

    JSONL_EXTENSIONS = {
        ".jsonl",
        ".ndjson",
    }

    MAX_ROWS = 10000
    MAX_COLUMNS = 200

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info
        self.path = Path(file_info.path)

        self.connection = None
        self.tables = []

        self.type_label = QLabel()
        self.info_label = QLabel()

        self.table_selector = QComboBox()
        self.table_selector.setMinimumWidth(220)

        self.reload_button = QPushButton(
            "再読み込み"
        )

        self.table = QTableWidget()

        self.tabs = QTabWidget()

        self._setup_ui()
        self._load_file()

    # ==================================================
    # UI
    # ==================================================

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        self.type_label.setText(
            f"データ: {self.path.name}"
        )

        header_layout.addWidget(
            self.type_label
        )

        header_layout.addStretch()

        header_layout.addWidget(
            self.reload_button
        )

        main_layout.addLayout(
            header_layout
        )

        controls_layout = QHBoxLayout()

        controls_layout.addWidget(
            QLabel("テーブル:")
        )

        controls_layout.addWidget(
            self.table_selector
        )

        controls_layout.addStretch()

        main_layout.addLayout(
            controls_layout
        )

        main_layout.addWidget(
            self.info_label
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSortingEnabled(
            True
        )

        main_layout.addWidget(
            self.table
        )

        self.reload_button.clicked.connect(
            self._reload
        )

        self.table_selector.currentTextChanged.connect(
            self._table_changed
        )

    # ==================================================
    # Load
    # ==================================================

    def _load_file(self):
        extension = self.path.suffix.lower()

        try:
            if extension in self.SQLITE_EXTENSIONS:
                self._load_sqlite()

            elif extension in self.PARQUET_EXTENSIONS:
                self._load_parquet()

            elif extension in self.JSONL_EXTENSIONS:
                self._load_json_lines()

            else:
                self._show_error(
                    "対応していないデータ形式です。"
                )

        except Exception as exc:
            self._show_error(
                "データを読み込めませんでした。",
                exc,
            )

    # ==================================================
    # SQLite
    # ==================================================

    def _load_sqlite(self):
        self._close_connection()

        self.connection = sqlite3.connect(
            f"file:{self.path.resolve()}?mode=ro",
            uri=True,
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )

        self.tables = [
            row[0]
            for row in cursor.fetchall()
        ]

        self.table_selector.blockSignals(
            True
        )

        self.table_selector.clear()

        self.table_selector.addItems(
            self.tables
        )

        self.table_selector.blockSignals(
            False
        )

        if not self.tables:
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)

            self.info_label.setText(
                "テーブルがありません。"
            )

            return

        self._show_sqlite_table(
            self.tables[0]
        )

    def _show_sqlite_table(
        self,
        table_name,
    ):
        if self.connection is None:
            return

        cursor = self.connection.cursor()

        escaped_name = (
            table_name.replace(
                '"',
                '""',
            )
        )

        query = (
            f'SELECT * FROM "{escaped_name}" '
            f"LIMIT {self.MAX_ROWS}"
        )

        cursor.execute(query)

        columns = [
            description[0]
            for description in cursor.description
        ]

        rows = cursor.fetchall()

        self._display_rows(
            columns,
            rows,
        )

        self.info_label.setText(
            f"テーブル: {table_name} / "
            f"{len(rows):,}行 / "
            f"{len(columns):,}列"
        )

    def _table_changed(
        self,
        table_name,
    ):
        if not table_name:
            return

        extension = self.path.suffix.lower()

        if extension in self.SQLITE_EXTENSIONS:
            try:
                self._show_sqlite_table(
                    table_name
                )

            except Exception as exc:
                self._show_error(
                    "テーブルを読み込めませんでした。",
                    exc,
                )

    # ==================================================
    # Parquet
    # ==================================================

    def _load_parquet(self):
        try:
            import pyarrow.parquet as pq

        except ImportError as exc:
            raise RuntimeError(
                "Parquetの読み込みには"
                "pyarrowが必要です。\n\n"
                "次のコマンドでインストールしてください:\n"
                "py -m pip install pyarrow"
            ) from exc

        parquet_file = pq.ParquetFile(
            self.path
        )

        schema = parquet_file.schema_arrow

        columns = [
            field.name
            for field in schema
        ]

        table = parquet_file.read(
            columns=columns[
                : self.MAX_COLUMNS
            ]
        )

        rows = table.to_pylist()

        rows = rows[
            : self.MAX_ROWS
        ]

        self.table_selector.clear()
        self.table_selector.setEnabled(
            False
        )

        self._display_dictionary_rows(
            rows,
            columns,
        )

        self.info_label.setText(
            f"Parquet / "
            f"{len(rows):,}行 / "
            f"{len(columns):,}列"
        )

    # ==================================================
    # JSONL / NDJSON
    # ==================================================

    def _load_json_lines(self):
        rows = []

        with self.path.open(
            "r",
            encoding="utf-8-sig",
            errors="replace",
        ) as file:
            for line_number, line in enumerate(
                file,
                start=1,
            ):
                if len(rows) >= self.MAX_ROWS:
                    break

                line = line.strip()

                if not line:
                    continue

                try:
                    value = json.loads(
                        line
                    )

                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"{line_number}行目のJSONを"
                        "解析できませんでした。\n"
                        f"{exc}"
                    ) from exc

                if isinstance(
                    value,
                    dict,
                ):
                    rows.append(value)

                else:
                    rows.append(
                        {
                            "value": value,
                        }
                    )

        columns = []

        for row in rows:
            if not isinstance(
                row,
                dict,
            ):
                continue

            for key in row.keys():
                if key not in columns:
                    columns.append(key)

        columns = columns[
            : self.MAX_COLUMNS
        ]

        self.table_selector.clear()
        self.table_selector.setEnabled(
            False
        )

        self._display_dictionary_rows(
            rows,
            columns,
        )

        self.info_label.setText(
            f"JSON Lines / "
            f"{len(rows):,}行 / "
            f"{len(columns):,}列"
        )

    # ==================================================
    # Display
    # ==================================================

    def _display_dictionary_rows(
        self,
        rows,
        columns,
    ):
        converted_rows = []

        for row in rows:
            converted = []

            if isinstance(
                row,
                dict,
            ):
                for column in columns:
                    converted.append(
                        row.get(column)
                    )

            else:
                converted.append(row)

            converted_rows.append(
                converted
            )

        self._display_rows(
            columns,
            converted_rows,
        )

    def _display_rows(
        self,
        columns,
        rows,
    ):
        self.table.setSortingEnabled(
            False
        )

        self.table.clear()

        self.table.setColumnCount(
            len(columns)
        )

        self.table.setRowCount(
            len(rows)
        )

        self.table.setHorizontalHeaderLabels(
            [
                str(column)
                for column in columns
            ]
        )

        for row_index, row in enumerate(
            rows
        ):
            for column_index in range(
                len(columns)
            ):
                if column_index >= len(row):
                    value = ""

                else:
                    value = row[
                        column_index
                    ]

                text = self._format_value(
                    value
                )

                item = QTableWidgetItem(
                    text
                )

                item.setFlags(
                    item.flags()
                    & ~Qt.ItemFlag.ItemIsEditable
                )

                self.table.setItem(
                    row_index,
                    column_index,
                    item,
                )

        self.table.resizeColumnsToContents()

        self.table.setSortingEnabled(
            True
        )

    @staticmethod
    def _format_value(value):
        if value is None:
            return ""

        if isinstance(
            value,
            (dict, list, tuple),
        ):
            try:
                return json.dumps(
                    value,
                    ensure_ascii=False,
                    separators=(
                        ",",
                        ":",
                    ),
                )

            except TypeError:
                return str(value)

        if isinstance(
            value,
            bytes,
        ):
            try:
                return value.decode(
                    "utf-8",
                    errors="replace",
                )

            except Exception:
                return repr(value)

        return str(value)

    # ==================================================
    # Reload / Error
    # ==================================================

    def _reload(self):
        self.table_selector.blockSignals(
            True
        )

        self.table_selector.setEnabled(
            True
        )

        self.table_selector.blockSignals(
            False
        )

        self._load_file()

    def _show_error(
        self,
        message,
        exception=None,
    ):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        if exception is not None:
            message = (
                f"{message}\n\n"
                f"{exception}"
            )

        self.info_label.setText(
            message
        )

        QMessageBox.warning(
            self,
            "Data Plugin",
            message,
        )

    # ==================================================
    # Cleanup
    # ==================================================

    def _close_connection(self):
        if self.connection is not None:
            try:
                self.connection.close()

            except Exception:
                pass

            self.connection = None

    def closeEvent(self, event):
        self._close_connection()

        super().closeEvent(
            event
        )