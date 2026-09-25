from pathlib import Path

from core.file_info import FileInfo
from core.plugin import FilePlugin


class TestPlugin(FilePlugin):
    name = "Test Plugin"
    version = "1.0.0"
    extensions = [".test"]

    def create_viewer(self, file_info, parent=None):
        return None


def test_plugin_extension():
    plugin = TestPlugin()

    info = FileInfo(
        Path("sample.test")
    )

    assert plugin.can_open(info)


def test_plugin_rejects_other_extension():
    plugin = TestPlugin()

    info = FileInfo(
        Path("sample.txt")
    )

    assert not plugin.can_open(info)