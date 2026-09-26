from pathlib import Path

from PySide6.QtCore import (
    QRegularExpression,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QTextCharFormat,
    QSyntaxHighlighter,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)


class CodeHighlighter(QSyntaxHighlighter):
    """軽量なコード用シンタックスハイライター。"""

    LANGUAGE_RULES = {
        "python": {
            "keywords": [
                "and",
                "as",
                "assert",
                "async",
                "await",
                "break",
                "case",
                "class",
                "continue",
                "def",
                "del",
                "elif",
                "else",
                "except",
                "finally",
                "for",
                "from",
                "global",
                "if",
                "import",
                "in",
                "is",
                "lambda",
                "match",
                "nonlocal",
                "not",
                "or",
                "pass",
                "raise",
                "return",
                "try",
                "while",
                "with",
                "yield",
            ],
            "types": [
                "bool",
                "bytearray",
                "bytes",
                "complex",
                "dict",
                "float",
                "frozenset",
                "int",
                "list",
                "object",
                "set",
                "str",
                "tuple",
            ],
            "comment": "#",
        },

        "javascript": {
            "keywords": [
                "as",
                "async",
                "await",
                "break",
                "case",
                "catch",
                "class",
                "const",
                "continue",
                "debugger",
                "default",
                "delete",
                "do",
                "else",
                "export",
                "extends",
                "finally",
                "for",
                "from",
                "function",
                "if",
                "import",
                "in",
                "instanceof",
                "let",
                "new",
                "of",
                "return",
                "static",
                "super",
                "switch",
                "this",
                "throw",
                "try",
                "typeof",
                "var",
                "void",
                "while",
                "with",
                "yield",
            ],
            "types": [
                "Array",
                "Boolean",
                "Date",
                "Error",
                "Function",
                "Map",
                "Number",
                "Object",
                "Promise",
                "Set",
                "String",
            ],
            "comment": "//",
        },

        "typescript": {
            "keywords": [
                "as",
                "async",
                "await",
                "break",
                "case",
                "catch",
                "class",
                "const",
                "continue",
                "default",
                "delete",
                "else",
                "export",
                "extends",
                "finally",
                "for",
                "from",
                "function",
                "if",
                "implements",
                "import",
                "in",
                "interface",
                "keyof",
                "let",
                "new",
                "of",
                "private",
                "protected",
                "public",
                "readonly",
                "return",
                "static",
                "super",
                "switch",
                "this",
                "throw",
                "try",
                "type",
                "typeof",
                "var",
                "void",
                "while",
                "with",
                "yield",
            ],
            "types": [
                "any",
                "boolean",
                "never",
                "number",
                "object",
                "string",
                "unknown",
                "void",
            ],
            "comment": "//",
        },

        "c": {
            "keywords": [
                "auto",
                "break",
                "case",
                "char",
                "const",
                "continue",
                "default",
                "do",
                "double",
                "else",
                "enum",
                "extern",
                "float",
                "for",
                "goto",
                "if",
                "inline",
                "int",
                "long",
                "register",
                "restrict",
                "return",
                "short",
                "signed",
                "sizeof",
                "static",
                "struct",
                "switch",
                "typedef",
                "union",
                "unsigned",
                "void",
                "volatile",
                "while",
            ],
            "types": [
                "bool",
                "size_t",
                "uint8_t",
                "uint16_t",
                "uint32_t",
                "uint64_t",
                "int8_t",
                "int16_t",
                "int32_t",
                "int64_t",
            ],
            "comment": "//",
        },

        "cpp": {
            "keywords": [
                "alignas",
                "alignof",
                "asm",
                "auto",
                "bool",
                "break",
                "case",
                "catch",
                "class",
                "const",
                "constexpr",
                "continue",
                "default",
                "delete",
                "do",
                "else",
                "enum",
                "explicit",
                "export",
                "extern",
                "false",
                "for",
                "friend",
                "goto",
                "if",
                "inline",
                "mutable",
                "namespace",
                "new",
                "noexcept",
                "nullptr",
                "operator",
                "private",
                "protected",
                "public",
                "return",
                "sizeof",
                "static",
                "struct",
                "switch",
                "template",
                "this",
                "throw",
                "true",
                "try",
                "typedef",
                "typename",
                "union",
                "using",
                "virtual",
                "void",
                "volatile",
                "while",
            ],
            "types": [
                "char",
                "double",
                "float",
                "int",
                "long",
                "short",
                "signed",
                "size_t",
                "unsigned",
                "wchar_t",
            ],
            "comment": "//",
        },

        "java": {
            "keywords": [
                "abstract",
                "assert",
                "boolean",
                "break",
                "byte",
                "case",
                "catch",
                "char",
                "class",
                "const",
                "continue",
                "default",
                "do",
                "double",
                "else",
                "enum",
                "extends",
                "final",
                "finally",
                "float",
                "for",
                "if",
                "implements",
                "import",
                "instanceof",
                "int",
                "interface",
                "long",
                "native",
                "new",
                "package",
                "private",
                "protected",
                "public",
                "return",
                "short",
                "static",
                "strictfp",
                "super",
                "switch",
                "synchronized",
                "this",
                "throw",
                "throws",
                "transient",
                "try",
                "void",
                "volatile",
                "while",
            ],
            "types": [
                "String",
                "Object",
                "Integer",
                "Double",
                "Float",
                "Boolean",
                "Long",
                "List",
                "Map",
                "Set",
            ],
            "comment": "//",
        },

        "csharp": {
            "keywords": [
                "abstract",
                "as",
                "base",
                "bool",
                "break",
                "byte",
                "case",
                "catch",
                "char",
                "checked",
                "class",
                "const",
                "continue",
                "decimal",
                "default",
                "delegate",
                "do",
                "double",
                "else",
                "enum",
                "event",
                "explicit",
                "extern",
                "false",
                "finally",
                "fixed",
                "float",
                "for",
                "foreach",
                "if",
                "implicit",
                "in",
                "int",
                "interface",
                "internal",
                "is",
                "lock",
                "long",
                "namespace",
                "new",
                "null",
                "object",
                "operator",
                "out",
                "override",
                "params",
                "private",
                "protected",
                "public",
                "readonly",
                "ref",
                "return",
                "sealed",
                "short",
                "sizeof",
                "stackalloc",
                "static",
                "string",
                "struct",
                "switch",
                "this",
                "throw",
                "true",
                "try",
                "typeof",
                "uint",
                "ulong",
                "unchecked",
                "unsafe",
                "ushort",
                "using",
                "virtual",
                "void",
                "volatile",
                "while",
            ],
            "types": [
                "String",
                "Object",
                "Task",
                "List",
                "Dictionary",
            ],
            "comment": "//",
        },

        "go": {
            "keywords": [
                "break",
                "case",
                "chan",
                "const",
                "continue",
                "default",
                "defer",
                "else",
                "fallthrough",
                "for",
                "func",
                "go",
                "goto",
                "if",
                "import",
                "interface",
                "map",
                "package",
                "range",
                "return",
                "select",
                "struct",
                "switch",
                "type",
                "var",
            ],
            "types": [
                "bool",
                "byte",
                "complex64",
                "complex128",
                "error",
                "float32",
                "float64",
                "int",
                "int8",
                "int16",
                "int32",
                "int64",
                "rune",
                "string",
                "uint",
                "uint8",
                "uint16",
                "uint32",
                "uint64",
                "uintptr",
            ],
            "comment": "//",
        },

        "rust": {
            "keywords": [
                "as",
                "async",
                "await",
                "break",
                "const",
                "continue",
                "crate",
                "dyn",
                "else",
                "enum",
                "extern",
                "false",
                "fn",
                "for",
                "if",
                "impl",
                "in",
                "let",
                "loop",
                "match",
                "mod",
                "move",
                "mut",
                "pub",
                "ref",
                "return",
                "self",
                "Self",
                "static",
                "struct",
                "super",
                "trait",
                "true",
                "type",
                "unsafe",
                "use",
                "where",
                "while",
            ],
            "types": [
                "bool",
                "char",
                "f32",
                "f64",
                "i8",
                "i16",
                "i32",
                "i64",
                "i128",
                "isize",
                "str",
                "String",
                "u8",
                "u16",
                "u32",
                "u64",
                "u128",
                "usize",
            ],
            "comment": "//",
        },

        "ruby": {
            "keywords": [
                "BEGIN",
                "END",
                "alias",
                "and",
                "begin",
                "break",
                "case",
                "class",
                "def",
                "defined",
                "do",
                "else",
                "elsif",
                "end",
                "ensure",
                "false",
                "for",
                "if",
                "in",
                "module",
                "next",
                "nil",
                "not",
                "or",
                "redo",
                "rescue",
                "retry",
                "return",
                "self",
                "super",
                "then",
                "true",
                "undef",
                "unless",
                "until",
                "when",
                "while",
                "yield",
            ],
            "types": [
                "Array",
                "Hash",
                "Integer",
                "String",
                "Symbol",
                "Time",
            ],
            "comment": "#",
        },

        "php": {
            "keywords": [
                "abstract",
                "and",
                "array",
                "as",
                "break",
                "callable",
                "case",
                "catch",
                "class",
                "clone",
                "const",
                "continue",
                "declare",
                "default",
                "do",
                "echo",
                "else",
                "elseif",
                "empty",
                "extends",
                "final",
                "finally",
                "for",
                "foreach",
                "function",
                "global",
                "if",
                "implements",
                "include",
                "instanceof",
                "interface",
                "namespace",
                "new",
                "or",
                "private",
                "protected",
                "public",
                "require",
                "return",
                "static",
                "switch",
                "throw",
                "trait",
                "try",
                "use",
                "var",
                "while",
                "xor",
            ],
            "types": [
                "bool",
                "float",
                "int",
                "iterable",
                "mixed",
                "object",
                "string",
            ],
            "comment": "//",
        },

        "sql": {
            "keywords": [
                "ALTER",
                "AND",
                "AS",
                "ASC",
                "BEGIN",
                "BY",
                "CASE",
                "CREATE",
                "DELETE",
                "DESC",
                "DISTINCT",
                "DROP",
                "ELSE",
                "END",
                "FROM",
                "GROUP",
                "HAVING",
                "INSERT",
                "INTO",
                "JOIN",
                "LEFT",
                "LIMIT",
                "NOT",
                "NULL",
                "ON",
                "OR",
                "ORDER",
                "OUTER",
                "PRIMARY",
                "REFERENCES",
                "RIGHT",
                "SELECT",
                "SET",
                "TABLE",
                "THEN",
                "UNION",
                "UPDATE",
                "VALUES",
                "WHEN",
                "WHERE",
            ],
            "types": [
                "BIGINT",
                "BOOLEAN",
                "CHAR",
                "DATE",
                "DECIMAL",
                "DOUBLE",
                "FLOAT",
                "INTEGER",
                "TEXT",
                "TIME",
                "TIMESTAMP",
                "VARCHAR",
            ],
            "comment": "--",
        },
    }

    EXTENSION_TO_LANGUAGE = {
        ".py": "python",
        ".pyw": "python",

        ".js": "javascript",
        ".jsx": "javascript",
        ".mjs": "javascript",
        ".cjs": "javascript",

        ".ts": "typescript",
        ".tsx": "typescript",

        ".c": "c",
        ".h": "c",

        ".cc": "cpp",
        ".cpp": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",

        ".java": "java",

        ".cs": "csharp",

        ".go": "go",

        ".rs": "rust",

        ".rb": "ruby",

        ".php": "php",

        ".sql": "sql",

        ".kt": "java",
        ".kts": "java",

        ".swift": "c",

        ".dart": "javascript",

        ".lua": "python",

        ".r": "python",

        ".sh": "python",
        ".bash": "python",
        ".zsh": "python",

        ".bat": "batch",
        ".cmd": "batch",

        ".ps1": "powershell",

        ".html": "html",
        ".htm": "html",

        ".xml": "html",

        ".css": "css",
        ".scss": "css",
        ".sass": "css",
        ".less": "css",

        ".json": "json",

        ".yaml": "yaml",
        ".yml": "yaml",

        ".toml": "yaml",

        ".asm": "c",
        ".v": "c",
        ".vhd": "c",
        ".vhdl": "c",
    }

    def __init__(self, document, language):
        super().__init__(document)

        self.language = language

        self.keyword_format = self._format(
            "#569CD6",
            bold=True,
        )

        self.type_format = self._format(
            "#4EC9B0",
        )

        self.string_format = self._format(
            "#CE9178",
        )

        self.number_format = self._format(
            "#B5CEA8",
        )

        self.comment_format = self._format(
            "#6A9955",
        )

        self.function_format = self._format(
            "#DCDCAA",
        )

        self.decorator_format = self._format(
            "#C586C0",
        )

        self.boolean_format = self._format(
            "#569CD6",
            bold=True,
        )

    @staticmethod
    def _format(
        color,
        bold=False,
    ):
        text_format = QTextCharFormat()

        text_format.setForeground(
            QColor(color)
        )

        if bold:
            font = QFont()
            font.setBold(True)
            text_format.setFont(font)

        return text_format

    def highlightBlock(self, text):
        if self.language == "html":
            self._highlight_html(text)
            return

        if self.language == "css":
            self._highlight_css(text)
            return

        if self.language == "json":
            self._highlight_json(text)
            return

        if self.language == "yaml":
            self._highlight_yaml(text)
            return

        if self.language == "batch":
            self._highlight_batch(text)
            return

        if self.language == "powershell":
            self._highlight_powershell(text)
            return

        self._highlight_generic(text)

    def _apply_regex(
        self,
        text,
        pattern,
        text_format,
    ):
        expression = QRegularExpression(
            pattern
        )

        iterator = expression.globalMatch(
            text
        )

        while iterator.hasNext():
            match = iterator.next()

            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                text_format,
            )

    def _highlight_generic(self, text):
        rules = self.LANGUAGE_RULES.get(
            self.language,
            {},
        )

        comment = rules.get(
            "comment"
        )

        if comment:
            escaped = (
                QRegularExpression.escape(
                    comment
                )
            )

            self._apply_regex(
                text,
                f"{escaped}.*$",
                self.comment_format,
            )

        self._apply_regex(
            text,
            r'"(?:\\.|[^"\\])*"',
            self.string_format,
        )

        self._apply_regex(
            text,
            r"'(?:\\.|[^'\\])*'",
            self.string_format,
        )

        self._apply_regex(
            text,
            r"\b(?:0[xX][0-9A-Fa-f]+|0[bB][01]+|\d+(?:\.\d+)?)\b",
            self.number_format,
        )

        keywords = rules.get(
            "keywords",
            [],
        )

        if keywords:
            pattern = (
                r"\b(?:"
                + "|".join(
                    QRegularExpression.escape(
                        keyword
                    )
                    for keyword in keywords
                )
                + r")\b"
            )

            self._apply_regex(
                text,
                pattern,
                self.keyword_format,
            )

        types = rules.get(
            "types",
            [],
        )

        if types:
            pattern = (
                r"\b(?:"
                + "|".join(
                    QRegularExpression.escape(
                        value
                    )
                    for value in types
                )
                + r")\b"
            )

            self._apply_regex(
                text,
                pattern,
                self.type_format,
            )

        self._apply_regex(
            text,
            r"\b(?:True|False|true|false|null|None|nil|NULL)\b",
            self.boolean_format,
        )

        self._apply_regex(
            text,
            r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()",
            self.function_format,
        )

        self._apply_regex(
            text,
            r"@[A-Za-z_][A-Za-z0-9_.]*",
            self.decorator_format,
        )

    def _highlight_html(self, text):
        self._apply_regex(
            text,
            r"<!--.*?-->",
            self.comment_format,
        )

        self._apply_regex(
            text,
            r"</?[A-Za-z][^>]*>",
            self.keyword_format,
        )

        self._apply_regex(
            text,
            r"\b[A-Za-z_:][A-Za-z0-9_.:-]*(?=\s*=)",
            self.type_format,
        )

        self._apply_regex(
            text,
            r'"(?:\\.|[^"\\])*"',
            self.string_format,
        )

        self._apply_regex(
            text,
            r"'(?:\\.|[^'\\])*'",
            self.string_format,
        )

        self._apply_regex(
            text,
            r"&[A-Za-z0-9#]+;",
            self.number_format,
        )

    def _highlight_css(self, text):
        self._apply_regex(
            text,
            r"/\*.*?\*/",
            self.comment_format,
        )

        self._apply_regex(
            text,
            r'"(?:\\.|[^"\\])*"',
            self.string_format,
        )

        self._apply_regex(
            text,
            r"'(?:\\.|[^'\\])*'",
            self.string_format,
        )

        self._apply_regex(
            text,
            r"#[A-Fa-f0-9]{3,8}\b",
            self.number_format,
        )

        self._apply_regex(
            text,
            r"\b\d+(?:\.\d+)?(?:px|em|rem|%|vh|vw|s|ms|deg)?\b",
            self.number_format,
        )

        self._apply_regex(
            text,
            r"--?[A-Za-z_-][A-Za-z0-9_-]*(?=\s*:)",
            self.type_format,
        )

        self._apply_regex(
            text,
            r"\b(?:color|background|display|position|margin|padding|width|height|font|border|grid|flex|content|transform|opacity)\b",
            self.keyword_format,
        )

    def _highlight_json(self, text):
        self._apply_regex(
            text,
            r'"(?:\\.|[^"\\])*"(?=\s*:)',
            self.keyword_format,
        )

        self._apply_regex(
            text,
            r'"(?:\\.|[^"\\])*"',
            self.string_format,
        )

        self._apply_regex(
            text,
            r"\b(?:true|false|null)\b",
            self.boolean_format,
        )

        self._apply_regex(
            text,
            r"-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b",
            self.number_format,
        )

    def _highlight_yaml(self, text):
        self._apply_regex(
            text,
            r"^\s*[-]?\s*[A-Za-z_][A-Za-z0-9_-]*(?=\s*:)",
            self.keyword_format,
        )

        self._apply_regex(
            text,
            r'"(?:\\.|[^"\\])*"',
            self.string_format,
        )

        self._apply_regex(
            text,
            r"'(?:[^']|'')*'",
            self.string_format,
        )

        self._apply_regex(
            text,
            r"\b(?:true|false|null|yes|no|on|off)\b",
            self.boolean_format,
        )

        self._apply_regex(
            text,
            r"-?\b\d+(?:\.\d+)?\b",
            self.number_format,
        )

        self._apply_regex(
            text,
            r"#.*$",
            self.comment_format,
        )

    def _highlight_batch(self, text):
        self._apply_regex(
            text,
            r"^\s*(?:REM\b.*|::.*)$",
            self.comment_format,
        )

        self._apply_regex(
            text,
            r"%[^%]+%",
            self.string_format,
        )

        self._apply_regex(
            text,
            r"\b(?:ECHO|SET|IF|ELSE|FOR|IN|DO|GOTO|CALL|PAUSE|EXIT|START|COPY|MOVE|DEL|MKDIR|RMDIR)\b",
            self.keyword_format,
        )

    def _highlight_powershell(self, text):
        self._apply_regex(
            text,
            r"#.*$",
            self.comment_format,
        )

        self._apply_regex(
            text,
            r'"(?:`.|[^"\\])*"',
            self.string_format,
        )

        self._apply_regex(
            text,
            r"'(?:''|[^'])*'",
            self.string_format,
        )

        self._apply_regex(
            text,
            r"\b(?:function|param|if|else|elseif|foreach|for|while|do|switch|return|class|filter|try|catch|finally|throw|break|continue|begin|process|end)\b",
            self.keyword_format,
        )

        self._apply_regex(
            text,
            r"\$[A-Za-z_][A-Za-z0-9_:]*",
            self.type_format,
        )

        self._apply_regex(
            text,
            r"\b(?:true|false|null)\b",
            self.boolean_format,
        )

        self._apply_regex(
            text,
            r"\b\d+(?:\.\d+)?\b",
            self.number_format,
        )


class TextViewer(QWidget):
    """テキスト・コードファイル表示用ビューア。"""

    TEXT_EXTENSIONS = {
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
    }

    CODE_EXTENSIONS = (
        set(
            CodeHighlighter.EXTENSION_TO_LANGUAGE.keys()
        )
        | {
            ".json",
            ".yaml",
            ".yml",
            ".toml",
        }
    )

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info
        self.file_path = Path(
            file_info.path
        )

        self.setWindowTitle(
            f"{file_info.name} - open"
        )

        self.editor = QPlainTextEdit(
            self
        )

        self.editor.setReadOnly(
            True
        )

        self.editor.setLineWrapMode(
            QPlainTextEdit.NoWrap
        )

        font = QFont(
            "Consolas"
        )

        font.setStyleHint(
            QFont.Monospace
        )

        font.setPointSize(10)

        self.editor.setFont(
            font
        )

        self.editor.setTabStopDistance(
            4
            * self.editor.fontMetrics().horizontalAdvance(
                " "
            )
        )

        self.info_label = QLabel(
            self
        )

        self.info_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        layout = QVBoxLayout(
            self
        )

        header_layout = QHBoxLayout()

        header_layout.addWidget(
            QLabel(
                "ファイル:"
            )
        )

        header_layout.addWidget(
            self.info_label,
            1,
        )

        layout.addLayout(
            header_layout
        )

        layout.addWidget(
            self.editor,
            1,
        )

        self.highlighter = None

        self._load_file()

    def _load_file(self):
        data = self.file_path.read_bytes()

        text, encoding = (
            self._decode_data(data)
        )

        self.editor.setPlainText(
            text
        )

        extension = (
            self.file_info.extension
        )

        language = (
            CodeHighlighter
            .EXTENSION_TO_LANGUAGE
            .get(extension)
        )

        if language:
            self.highlighter = (
                CodeHighlighter(
                    self.editor.document(),
                    language,
                )
            )

        size = self.file_info.size

        self.info_label.setText(
            f"{self.file_info.name}"
            f"  |  {encoding}"
            f"  |  {self._format_size(size)}"
        )

    @staticmethod
    def _decode_data(data):
        encodings = [
            "utf-8-sig",
            "utf-8",
            "cp932",
            "shift_jis",
            "euc_jp",
            "iso-2022-jp",
            "latin-1",
        ]

        for encoding in encodings:
            try:
                return (
                    data.decode(encoding),
                    encoding,
                )
            except UnicodeDecodeError:
                continue

        return (
            data.decode(
                "utf-8",
                errors="replace",
            ),
            "utf-8 (replacement)",
        )

    @staticmethod
    def _format_size(size):
        if size < 1024:
            return f"{size} B"

        if size < 1024 * 1024:
            return (
                f"{size / 1024:.1f} KB"
            )

        if size < 1024 * 1024 * 1024:
            return (
                f"{size / (1024 * 1024):.1f} MB"
            )

        return (
            f"{size / (1024 * 1024 * 1024):.1f} GB"
        )