class FileFusionError(Exception):
    """FileFusionの基本例外。"""


class PluginError(FileFusionError):
    """プラグイン関連のエラー。"""


class PluginLoadError(PluginError):
    """プラグインの読み込みに失敗した場合のエラー。"""


class UnsupportedFileError(FileFusionError):
    """対応していないファイルを開こうとした場合のエラー。"""