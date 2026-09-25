from bisect import bisect_left
import math

from PySide6.QtCore import (
    QTimer,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .midi_parser import MIDIParser
from .midi_player import MIDIPlayer


class PianoRollWidget(QWidget):
    """超軽量MIDIピアノロール。"""

    KEYBOARD_WIDTH = 55
    KEY_HEIGHT = 5

    def __init__(self, parent=None):
        super().__init__(parent)

        self.midi_data = None
        self.position = 0.0

        self.zoom_x = 70.0

        self._note_starts = []

        self._background = None
        self._background_size = None

        self.setAttribute(
            Qt.WidgetAttribute.WA_OpaquePaintEvent
        )

    def set_midi_data(self, midi_data):
        self.midi_data = midi_data

        self._note_starts = [
            note.start
            for note in midi_data.notes
        ]

        self.position = 0.0

        self._invalidate_background()

        self.update()

    def set_position(self, position):
        # 小さな変化は無視
        if abs(
            position - self.position
        ) < 0.03:
            return

        self.position = position

        self.update()

    def resizeEvent(self, event):
        self._invalidate_background()

        super().resizeEvent(event)

    def _invalidate_background(self):
        self._background = None
        self._background_size = None

    def _make_background(self):
        width = self.width()
        height = self.height()

        if width <= 0 or height <= 0:
            return

        pixmap = QPixmap(
            width,
            height,
        )

        pixmap.fill(
            QColor("#101318")
        )

        painter = QPainter(pixmap)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            False,
        )

        # 背景
        painter.fillRect(
            0,
            0,
            width,
            height,
            QColor("#101318"),
        )

        roll_width = (
            width
            - self.KEYBOARD_WIDTH
        )

        # 黒鍵部分の背景だけ描画
        painter.setPen(
            Qt.PenStyle.NoPen
        )

        for note in range(128):

            y = (
                height
                - (
                    (note + 1)
                    * self.KEY_HEIGHT
                )
            )

            if y < 0:
                continue

            if note % 12 in (
                1,
                3,
                6,
                8,
                10,
            ):
                painter.fillRect(
                    self.KEYBOARD_WIDTH,
                    y,
                    roll_width,
                    self.KEY_HEIGHT,
                    QColor("#171b21"),
                )

        # 鍵盤
        for note in range(128):

            y = (
                height
                - (
                    (note + 1)
                    * self.KEY_HEIGHT
                )
            )

            if y < 0:
                continue

            black = (
                note % 12
                in (
                    1,
                    3,
                    6,
                    8,
                    10,
                )
            )

            if black:
                painter.fillRect(
                    0,
                    y,
                    self.KEYBOARD_WIDTH,
                    self.KEY_HEIGHT,
                    QColor("#292d34"),
                )
            else:
                painter.fillRect(
                    0,
                    y,
                    self.KEYBOARD_WIDTH,
                    self.KEY_HEIGHT,
                    QColor("#dedede"),
                )

        painter.end()

        self._background = pixmap
        self._background_size = (
            width,
            height,
        )

    def paintEvent(self, event):
        width = self.width()
        height = self.height()

        if width <= 0 or height <= 0:
            return

        size = (
            width,
            height,
        )

        if (
            self._background is None
            or self._background_size != size
        ):
            self._make_background()

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            False,
        )

        # 背景を一枚貼るだけ
        painter.drawPixmap(
            0,
            0,
            self._background,
        )

        if self.midi_data is None:
            painter.end()
            return

        roll_width = (
            width
            - self.KEYBOARD_WIDTH
        )

        if roll_width <= 0:
            painter.end()
            return

        visible_seconds = (
            roll_width
            / self.zoom_x
        )

        start_time = max(
            0.0,
            self.position
            - visible_seconds * 0.20,
        )

        end_time = (
            start_time
            + visible_seconds
        )

        # 時間グリッド
        self._draw_grid(
            painter,
            start_time,
            end_time,
            height,
        )

        # ノート
        self._draw_notes(
            painter,
            start_time,
            end_time,
            height,
        )

        # 再生位置
        x = (
            self.KEYBOARD_WIDTH
            + (
                self.position
                - start_time
            )
            * self.zoom_x
        )

        painter.setPen(
            QPen(
                QColor("#ffffff"),
                1,
            )
        )

        painter.drawLine(
            int(x),
            0,
            int(x),
            height,
        )

        painter.end()

    def _draw_grid(
        self,
        painter,
        start_time,
        end_time,
        height,
    ):
        visible = (
            end_time - start_time
        )

        if visible > 60:
            step = 10.0
        elif visible > 30:
            step = 5.0
        elif visible > 15:
            step = 2.0
        else:
            step = 1.0

        painter.setPen(
            QPen(
                QColor("#242931"),
                1,
            )
        )

        current = (
            math.floor(
                start_time / step
            )
            * step
        )

        while current <= end_time:

            x = (
                self.KEYBOARD_WIDTH
                + (
                    current
                    - start_time
                )
                * self.zoom_x
            )

            painter.drawLine(
                int(x),
                0,
                int(x),
                height,
            )

            current += step

    def _draw_notes(
        self,
        painter,
        start_time,
        end_time,
        height,
    ):
        notes = self.midi_data.notes

        if not notes:
            return

        index = bisect_left(
            self._note_starts,
            start_time,
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        for note in notes[index:]:

            if note.start > end_time:
                break

            if note.end < start_time:
                continue

            y = (
                height
                - (
                    (note.note + 1)
                    * self.KEY_HEIGHT
                )
            )

            if (
                y < 0
                or y > height
            ):
                continue

            x = (
                self.KEYBOARD_WIDTH
                + (
                    note.start
                    - start_time
                )
                * self.zoom_x
            )

            width = max(
                1,
                int(
                    note.duration
                    * self.zoom_x
                ),
            )

            # 3段階だけ
            if note.velocity >= 100:
                painter.fillRect(
                    int(x),
                    int(y),
                    width,
                    self.KEY_HEIGHT - 1,
                    QColor("#72b5ff"),
                )

            elif note.velocity >= 60:
                painter.fillRect(
                    int(x),
                    int(y),
                    width,
                    self.KEY_HEIGHT - 1,
                    QColor("#4b8fd8"),
                )

            else:
                painter.fillRect(
                    int(x),
                    int(y),
                    width,
                    self.KEY_HEIGHT - 1,
                    QColor("#356aa2"),
                )


class MIDIViewer(QWidget):
    """MIDIファイルビューア。"""

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info

        self.parser = MIDIParser()
        self.player = MIDIPlayer()

        self.midi_data = None

        self.setWindowTitle(
            f"MIDI - {file_info.name}"
        )

        self._build_ui()

        self._load_file()

        self.timer = QTimer(self)

        # GUIは10FPS
        self.timer.setInterval(100)

        self.timer.timeout.connect(
            self._update_position
        )

    def _build_ui(self):
        layout = QVBoxLayout(self)

        info_layout = QHBoxLayout()

        self.info_label = QLabel(
            "MIDIを読み込み中..."
        )

        info_layout.addWidget(
            self.info_label
        )

        info_layout.addStretch()

        self.output_combo = QComboBox()

        self.output_combo.setMinimumWidth(
            220
        )

        # 接続は最初に1回だけ
        self.output_combo.currentTextChanged.connect(
            self._change_output
        )

        info_layout.addWidget(
            self.output_combo
        )

        layout.addLayout(
            info_layout
        )

        self.piano_roll = PianoRollWidget()

        layout.addWidget(
            self.piano_roll,
            1,
        )

        controls = QHBoxLayout()

        self.play_button = QPushButton(
            "▶ 再生"
        )

        self.play_button.clicked.connect(
            self._toggle_play
        )

        controls.addWidget(
            self.play_button
        )

        self.stop_button = QPushButton(
            "■ 停止"
        )

        self.stop_button.clicked.connect(
            self._stop
        )

        controls.addWidget(
            self.stop_button
        )

        self.slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.slider.setRange(
            0,
            1000,
        )

        self.slider.sliderMoved.connect(
            self._seek_slider
        )

        controls.addWidget(
            self.slider,
            1,
        )

        self.time_label = QLabel(
            "0:00 / 0:00"
        )

        controls.addWidget(
            self.time_label
        )

        layout.addLayout(
            controls
        )

    def _load_file(self):
        try:
            self.midi_data = (
                self.parser.parse(
                    self.file_info.path
                )
            )

            self.piano_roll.set_midi_data(
                self.midi_data
            )

            self.player.load(
                self.midi_data
            )

            self._setup_outputs()

            self.info_label.setText(
                f"{self.midi_data.filename} | "
                f"{self.midi_data.note_count:,} notes | "
                f"{self.midi_data.tracks} tracks | "
                f"{self.midi_data.tempo_bpm:.1f} BPM"
            )

            self._update_time_label()

        except Exception as exc:
            self.info_label.setText(
                f"読み込みエラー: {exc}"
            )

    def _setup_outputs(self):
        self.output_combo.blockSignals(
            True
        )

        self.output_combo.clear()

        outputs = (
            self.player.get_outputs()
        )

        if not outputs:
            self.output_combo.addItem(
                "MIDI出力なし（表示のみ）"
            )

            self.output_combo.blockSignals(
                False
            )

            return

        self.output_combo.addItems(
            outputs
        )

        self.player.open_output(
            outputs[0]
        )

        self.output_combo.blockSignals(
            False
        )

    def _change_output(self, name):
        if (
            not name
            or name.startswith(
                "MIDI出力なし"
            )
        ):
            return

        self.player.open_output(
            name
        )

    def _toggle_play(self):
        if not self.player.is_available():
            self._setup_outputs()

        if self.player.playing:
            self.player.pause()

            self.play_button.setText(
                "▶ 再生"
            )

            self.timer.stop()

            return

        if self.player.play():
            self.play_button.setText(
                "⏸ 一時停止"
            )

            self.timer.start()

    def _stop(self):
        self.player.stop()

        self.play_button.setText(
            "▶ 再生"
        )

        self.timer.stop()

        self.piano_roll.set_position(
            0.0
        )

        self.slider.setValue(0)

        self._update_time_label()

    def _seek_slider(self, value):
        if not self.midi_data:
            return

        position = (
            value / 1000.0
        ) * self.midi_data.length

        self.player.seek(
            position
        )

        self.piano_roll.set_position(
            position
        )

        self._update_time_label()

    def _update_position(self):
        position = (
            self.player.get_position()
        )

        self.piano_roll.set_position(
            position
        )

        if self.midi_data:

            length = (
                self.midi_data.length
            )

            if length > 0:
                value = int(
                    position
                    / length
                    * 1000
                )

                self.slider.setValue(
                    max(
                        0,
                        min(
                            1000,
                            value,
                        ),
                    )
                )

        self._update_time_label()

        if not self.player.playing:
            self.timer.stop()

            self.play_button.setText(
                "▶ 再生"
            )

    def _update_time_label(self):
        position = (
            self.player.get_position()
        )

        duration = (
            self.midi_data.length
            if self.midi_data
            else 0
        )

        self.time_label.setText(
            f"{self._format_time(position)}"
            f" / "
            f"{self._format_time(duration)}"
        )

    @staticmethod
    def _format_time(seconds):
        seconds = max(
            0,
            int(seconds),
        )

        minutes = seconds // 60
        seconds %= 60

        return (
            f"{minutes}:{seconds:02d}"
        )

    def closeEvent(self, event):
        self.timer.stop()

        self.player.shutdown()

        super().closeEvent(event)