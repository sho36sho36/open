from core.plugin import FilePlugin

from plugins.builtin.office.office_viewer import (
    OfficeViewer,
)


class OfficePlugin(FilePlugin):
    """Microsoft Office / OpenDocumentファイル対応プラグイン。"""

    name = "Office Plugin"
    version = "2.0.0"

    description = (
        "Spreadsheet、Document、Presentationなどの"
        "Office系ファイルを表示する共通プラグインです。"
    )

    extensions = [
        # Spreadsheet
        ".xlsx",
        ".ods",

        # Document
        ".docx",
        ".odt",
        ".rtf",

        # Presentation
        ".pptx",
        ".odp",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return OfficeViewer(
            file_info,
            parent,
        )