from pathlib import Path

from PySide6.QtCore import (
    QUrl,
    Qt,
)
from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaPlayer,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class AudioViewer(QWidget):
    """一般音声ファイル用の軽量プレイヤー。"""

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)

        self.player.setAudioOutput(
            self.audio_output
        )

        self.audio_output.setVolume(1.0)

        self._duration = 0
        self._updating_slider = False

        self._build_ui()
        self._connect_signals()
        self._load_file()

    def _build_ui(self):
        self.setMinimumSize(
            600,
            300,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )
        layout.setSpacing(12)

        self.title_label = QLabel(
            self.file_info.name
        )

        self.title_label.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        self.title_label.setWordWrap(True)

        layout.addWidget(
            self.title_label
        )

        self.format_label = QLabel(
            self._format_text()
        )

        self.format_label.setStyleSheet(
            """
            QLabel {
                color: #888888;
                font-size: 13px;
            }
            """
        )

        layout.addWidget(
            self.format_label
        )

        layout.addStretch()

        self.position_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.position_slider.setRange(
            0,
            0,
        )

        self.position_slider.setSingleStep(
            1000
        )

        layout.addWidget(
            self.position_slider
        )

        time_layout = QHBoxLayout()

        self.position_label = QLabel(
            "00:00"
        )

        self.duration_label = QLabel(
            "00:00"
        )

        time_layout.addWidget(
            self.position_label
        )

        time_layout.addStretch()

        time_layout.addWidget(
            self.duration_label
        )

        layout.addLayout(
            time_layout
        )

        controls = QHBoxLayout()

        self.stop_button = QPushButton(
            "⏹ 停止"
        )

        self.play_button = QPushButton(
            "▶ 再生"
        )

        self.pause_button = QPushButton(
            "⏸ 一時停止"
        )

        controls.addStretch()

        controls.addWidget(
            self.stop_button
        )

        controls.addWidget(
            self.play_button
        )

        controls.addWidget(
            self.pause_button
        )

        controls.addStretch()

        layout.addLayout(
            controls
        )

        volume_layout = QHBoxLayout()

        self.volume_label = QLabel(
            "🔊 音量"
        )

        self.volume_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.volume_slider.setRange(
            0,
            100,
        )

        self.volume_slider.setValue(
            100
        )

        self.volume_slider.setMaximumWidth(
            220
        )

        volume_layout.addStretch()

        volume_layout.addWidget(
            self.volume_label
        )

        volume_layout.addWidget(
            self.volume_slider
        )

        volume_layout.addStretch()

        layout.addLayout(
            volume_layout
        )

        self.status_label = QLabel(
            "読み込み中..."
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #777777;
            }
            """
        )

        layout.addWidget(
            self.status_label
        )

        layout.addStretch()

    def _connect_signals(self):
        self.play_button.clicked.connect(
            self.play
        )

        self.pause_button.clicked.connect(
            self.pause
        )

        self.stop_button.clicked.connect(
            self.stop
        )

        self.position_slider.sliderMoved.connect(
            self._slider_moved
        )

        self.position_slider.sliderPressed.connect(
            self._slider_pressed
        )

        self.position_slider.sliderReleased.connect(
            self._slider_released
        )

        self.volume_slider.valueChanged.connect(
            self._volume_changed
        )

        self.player.positionChanged.connect(
            self._position_changed
        )

        self.player.durationChanged.connect(
            self._duration_changed
        )

        self.player.playbackStateChanged.connect(
            self._playback_state_changed
        )

        self.player.mediaStatusChanged.connect(
            self._media_status_changed
        )

        self.player.errorOccurred.connect(
            self._error_occurred
        )

    def _load_file(self):
        path = Path(
            self.file_info.path
        )

        if not path.exists():
            self.status_label.setText(
                "ファイルが存在しません。"
            )
            return

        url = QUrl.fromLocalFile(
            str(path.resolve())
        )

        self.player.setSource(url)

        self.status_label.setText(
            "再生準備完了"
        )

    def _format_text(self):
        extension = (
            self.file_info.extension
            .upper()
        )

        size = self.file_info.size

        if size < 1024:
            size_text = f"{size} B"

        elif size < 1024 * 1024:
            size_text = (
                f"{size / 1024:.1f} KB"
            )

        else:
            size_text = (
                f"{size / (1024 * 1024):.1f} MB"
            )

        return (
            f"形式: {extension}    "
            f"サイズ: {size_text}"
        )

    def play(self):
        self.player.play()

        self.status_label.setText(
            "再生中"
        )

    def pause(self):
        self.player.pause()

        self.status_label.setText(
            "一時停止"
        )

    def stop(self):
        self.player.stop()

        self.status_label.setText(
            "停止"
        )

    def _position_changed(self, position):
        if not self._updating_slider:
            self.position_slider.setValue(
                position
            )

        self.position_label.setText(
            self._format_time(position)
        )

    def _duration_changed(self, duration):
        self._duration = duration

        self.position_slider.setRange(
            0,
            max(0, duration),
        )

        self.duration_label.setText(
            self._format_time(duration)
        )

    def _slider_pressed(self):
        self._updating_slider = True

    def _slider_moved(self, position):
        self.position_label.setText(
            self._format_time(position)
        )

    def _slider_released(self):
        position = (
            self.position_slider.value()
        )

        self.player.setPosition(
            position
        )

        self._updating_slider = False

    def _volume_changed(self, value):
        self.audio_output.setVolume(
            value / 100.0
        )

    def _playback_state_changed(
        self,
        state,
    ):
        if state == (
            QMediaPlayer.PlaybackState.PlayingState
        ):
            self.status_label.setText(
                "再生中"
            )

        elif state == (
            QMediaPlayer.PlaybackState.PausedState
        ):
            self.status_label.setText(
                "一時停止"
            )

        else:
            self.status_label.setText(
                "停止"
            )

    def _media_status_changed(
        self,
        status,
    ):
        if status == (
            QMediaPlayer.MediaStatus.EndOfMedia
        ):
            self.status_label.setText(
                "再生終了"
            )

    def _error_occurred(
        self,
        error,
        error_string,
    ):
        if error == (
            QMediaPlayer.Error.NoError
        ):
            return

        message = error_string.strip()

        if not message:
            message = (
                "この音声ファイルを再生できません。"
            )

        self.status_label.setText(
            f"再生エラー: {message}"
        )

    @staticmethod
    def _format_time(milliseconds):
        total_seconds = max(
            0,
            int(milliseconds / 1000),
        )

        hours = total_seconds // 3600
        minutes = (
            total_seconds % 3600
        ) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    def closeEvent(self, event):
        self.player.stop()
        self.player.setSource(QUrl())

        super().closeEvent(event)