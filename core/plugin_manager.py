import importlib.util
import inspect
from pathlib import Path

from .exceptions import PluginLoadError
from .plugin import FilePlugin


class PluginManager:
    """FileFusionプラグインを管理します。"""

    PLUGIN_ENTRY_FILE = "plugin.py"

    def __init__(self, plugin_directories=None):
        self.plugin_directories = [
            Path(directory)
            for directory in (plugin_directories or [])
        ]

        self.plugins = []

    def register(self, plugin):
        """プラグインを登録します。"""

        if not isinstance(plugin, FilePlugin):
            raise TypeError(
                "FilePluginを継承したプラグインのみ登録できます。"
            )

        # 同じプラグインクラスの重複登録を防止
        for existing in self.plugins:
            if type(existing) is type(plugin):
                return existing

        self.plugins.append(plugin)

        return plugin

    def discover(self):
        """
        プラグインを検索します。

        各プラグインディレクトリの中にある
        plugin.pyだけをエントリーポイントとして読み込みます。

        これにより、

            plugin.py
            midi_parser.py
            midi_player.py
            midi_viewer.py

        のような複数ファイル構成のプラグインを
        安全に扱えます。
        """

        for directory in self.plugin_directories:
            if not directory.exists():
                continue

            if not directory.is_dir():
                continue

            self._discover_directory(directory)

    def _discover_directory(self, directory):
        """
        ディレクトリ以下からplugin.pyを検索します。
        """

        for entry_file in directory.rglob(
            self.PLUGIN_ENTRY_FILE
        ):
            if entry_file.name.startswith("_"):
                continue

            self._load_file(entry_file)

    def _load_file(self, file):
        """plugin.pyからプラグインを読み込みます。"""

        module_name = self._create_module_name(
            file
        )

        try:
            spec = (
                importlib.util.spec_from_file_location(
                    module_name,
                    file,
                )
            )

            if (
                spec is None
                or spec.loader is None
            ):
                raise PluginLoadError(
                    f"モジュールを読み込めません: {file}"
                )

            module = (
                importlib.util.module_from_spec(
                    spec
                )
            )

            # sys.modulesへ登録することで、
            # プラグイン内部のimportを安定させる。
            import sys

            sys.modules[module_name] = module

            spec.loader.exec_module(
                module
            )

            self._register_module_plugins(
                module
            )

        except Exception as exc:
            raise PluginLoadError(
                f"プラグイン読み込み失敗: {file}\n"
                f"{exc}"
            ) from exc

    @staticmethod
    def _create_module_name(file):
        """
        ファイルパスから安全なモジュール名を作ります。
        """

        parts = file.with_suffix("").parts

        safe_parts = []

        for part in parts[-5:]:
            safe_part = "".join(
                character
                if character.isalnum()
                else "_"
                for character in part
            )

            safe_parts.append(
                safe_part
            )

        return (
            "filefusion_plugin_"
            + "_".join(safe_parts)
        )

    def _register_module_plugins(
        self,
        module,
    ):
        """モジュール内のPluginクラスを登録します。"""

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):
            if (
                issubclass(obj, FilePlugin)
                and obj is not FilePlugin
                and not inspect.isabstract(obj)
            ):
                self.register(obj())

    def initialize_all(self):
        """全プラグインを初期化します。"""

        for plugin in self.plugins:
            plugin.initialize()

    def shutdown_all(self):
        """全プラグインを終了します。"""

        for plugin in reversed(
            self.plugins
        ):
            plugin.shutdown()

    def find_plugin(self, file_info):
        """ファイルを開けるプラグインを探します。"""

        for plugin in self.plugins:
            if plugin.can_open(file_info):
                return plugin

        return None

    def find_plugins(self, file_info):
        """ファイルを開ける全プラグインを返します。"""

        return [
            plugin
            for plugin in self.plugins
            if plugin.can_open(file_info)
        ]

    def all_plugins(self):
        """登録済みプラグインを返します。"""

        return list(self.plugins)