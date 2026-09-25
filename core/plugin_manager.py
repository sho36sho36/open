import importlib.util
import inspect
from pathlib import Path

from .exceptions import PluginLoadError
from .plugin import FilePlugin


class PluginManager:
    """FileFusionプラグインを管理します。"""

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

        self.plugins.append(plugin)

        return plugin

    def discover(self):
        """プラグインディレクトリを検索します。"""

        for directory in self.plugin_directories:
            if not directory.exists():
                continue

            if not directory.is_dir():
                continue

            for file in directory.rglob("*.py"):
                if file.name.startswith("_"):
                    continue

                self._load_file(file)

    def _load_file(self, file):
        """Pythonファイルからプラグインを読み込みます。"""

        module_name = (
            "filefusion_plugin_"
            + "_".join(file.with_suffix("").parts[-3:])
        )

        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                file,
            )

            if spec is None or spec.loader is None:
                raise PluginLoadError(
                    f"モジュールを読み込めません: {file}"
                )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

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

        except Exception as exc:
            raise PluginLoadError(
                f"プラグイン読み込み失敗: {file}\n{exc}"
            ) from exc

    def initialize_all(self):
        for plugin in self.plugins:
            plugin.initialize()

    def shutdown_all(self):
        for plugin in reversed(self.plugins):
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
        return list(self.plugins)