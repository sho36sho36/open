from core.plugin import FilePlugin

from plugins.builtin.midi.midi_viewer import (
    MIDIViewer,
)


class MIDIPlugin(FilePlugin):
    """MIDIファイル対応プラグイン。"""

    name = "MIDI Plugin"
    version = "1.0.1"

    description = (
        "MIDIファイルを解析・再生し、"
        "ピアノロールとして表示します。"
    )

    extensions = [
        ".mid",
        ".midi",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return MIDIViewer(
            file_info,
            parent,
        )