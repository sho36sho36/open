from core.plugin import FilePlugin

from plugins.builtin.text.text_viewer import TextViewer


class TextCodePlugin(FilePlugin):
    """テキスト・コードファイルに対応する共通プラグイン。"""

    name = "Text / Code Plugin"
    version = "1.4.0"

    description = (
        "テキストファイルを表示し、"
        "プログラムコードをシンタックスハイライトします。"
    )

    extensions = [
        # テキスト
        ".txt",
        ".log",
        ".csv",
        ".tsv",
        ".ini",
        ".cfg",
        ".conf",
        ".properties",
        ".md",
        ".markdown",

        # Python
        ".py",
        ".pyw",

        # JavaScript / TypeScript
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".mjs",
        ".cjs",

        # Web
        ".html",
        ".htm",
        ".css",
        ".scss",
        ".sass",
        ".less",

        # JSON / XML / 設定
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".toml",

        # C / C++
        ".c",
        ".h",
        ".cc",
        ".cpp",
        ".cxx",
        ".hpp",

        # Java / Kotlin
        ".java",
        ".kt",
        ".kts",

        # C#
        ".cs",

        # Go
        ".go",

        # Rust
        ".rs",

        # Swift
        ".swift",

        # Dart
        ".dart",

        # Lua
        ".lua",

        # Ruby
        ".rb",

        # PHP
        ".php",

        # R
        ".r",

        # SQL
        ".sql",

        # Shell
        ".sh",
        ".bash",
        ".zsh",

        # Windows
        ".bat",
        ".cmd",
        ".ps1",

        # その他
        ".asm",
        ".v",
        ".vhd",
        ".vhdl",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return TextViewer(
            file_info,
            parent,
        )