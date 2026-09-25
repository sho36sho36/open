from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaPlayer,
)
from PySide6.QtMultimediaWidgets import (
    QVideoWidget,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class VideoViewer(QWidget):
    """一般的な動画ファイル用のビューア。"""

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info
        self.is_fullscreen = False

        self.player = QMediaPlayer(self)

        self.audio_output = QAudioOutput(self)

        self.video_widget = QVideoWidget(self)

        self.player.setAudioOutput(
            self.audio_output
        )

        self.player.setVideoOutput(
            self.video_widget
        )

        self._build_ui()
        self._connect_signals()
        self._load_file()

    def _build_ui(self):
        self.setMinimumSize(
            800,
            600,
        )

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        self.layout.setSpacing(8)

        self.header = QHBoxLayout()

        self.title_label = QLabel(
            self.file_info.name
        )

        self.title_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        self.title_label.setWordWrap(True)

        self.header.addWidget(
            self.title_label,
            1,
        )

        self.info_label = QLabel(
            ""
        )

        self.info_label.setStyleSheet(
            """
            QLabel {
                color: #888888;
                font-size: 12px;
            }
            """
        )

        self.header.addWidget(
            self.info_label
        )

        self.layout.addLayout(
            self.header
        )

        self.video_widget.setStyleSheet(
            """
            QVideoWidget {
                background: #000000;
            }
            """
        )

        self.layout.addWidget(
            self.video_widget,
            1,
        )

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

        self.position_slider.setPageStep(
            5000
        )

        self.layout.addWidget(
            self.position_slider
        )

        self.time_layout = QHBoxLayout()

        self.position_label = QLabel(
            "00:00"
        )

        self.duration_label = QLabel(
            "00:00"
        )

        self.time_layout.addWidget(
            self.position_label
        )

        self.time_layout.addStretch()

        self.time_layout.addWidget(
            self.duration_label
        )

        self.layout.addLayout(
            self.time_layout
        )

        self.controls = QHBoxLayout()

        self.play_button = QPushButton(
            "▶ 再生"
        )

        self.pause_button = QPushButton(
            "⏸ 一時停止"
        )

        self.stop_button = QPushButton(
            "⏹ 停止"
        )

        self.backward_button = QPushButton(
            "⏪ 5秒"
        )

        self.forward_button = QPushButton(
            "5秒 ⏩"
        )

        self.mute_button = QPushButton(
            "🔊"
        )

        self.fullscreen_button = QPushButton(
            "⛶ 全画面"
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

        self.volume_slider.setFixedWidth(
            120
        )

        self.controls.addStretch()

        self.controls.addWidget(
            self.backward_button
        )

        self.controls.addWidget(
            self.play_button
        )

        self.controls.addWidget(
            self.pause_button
        )

        self.controls.addWidget(
            self.stop_button
        )

        self.controls.addWidget(
            self.forward_button
        )

        self.controls.addWidget(
            self.mute_button
        )

        self.controls.addWidget(
            self.volume_slider
        )

        self.controls.addWidget(
            self.fullscreen_button
        )

        self.controls.addStretch()

        self.layout.addLayout(
            self.controls
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

        self.layout.addWidget(
            self.status_label
        )

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

        self.backward_button.clicked.connect(
            self.seek_backward
        )

        self.forward_button.clicked.connect(
            self.seek_forward
        )

        self.mute_button.clicked.connect(
            self.toggle_mute
        )

        self.fullscreen_button.clicked.connect(
            self.toggle_fullscreen
        )

        self.position_slider.sliderMoved.connect(
            self.seek
        )

        self.volume_slider.valueChanged.connect(
            self.set_volume
        )

        self.player.positionChanged.connect(
            self._on_position_changed
        )

        self.player.durationChanged.connect(
            self._on_duration_changed
        )

        self.player.mediaStatusChanged.connect(
            self._on_media_status_changed
        )

        self.player.errorOccurred.connect(
            self._on_error
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

        if not path.is_file():
            self.status_label.setText(
                "ファイルではありません。"
            )
            return

        self.info_label.setText(
            self._format_info()
        )

        self.player.setSource(
            QUrl.fromLocalFile(
                str(path.resolve())
            )
        )

        self.status_label.setText(
            "動画を読み込みました。"
        )

    def _format_info(self):
        size = self.file_info.size

        if size < 1024:
            size_text = f"{size} B"

        elif size < 1024 * 1024:
            size_text = (
                f"{size / 1024:.1f} KB"
            )

        elif size < 1024 * 1024 * 1024:
            size_text = (
                f"{size / (1024 * 1024):.1f} MB"
            )

        else:
            size_text = (
                f"{size / (1024 * 1024 * 1024):.2f} GB"
            )

        extension = (
            self.file_info.extension.upper()
        )

        return (
            f"{extension}    "
            f"{size_text}"
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

    def seek(self, position):
        self.player.setPosition(
            position
        )

    def seek_backward(self):
        position = max(
            0,
            self.player.position() - 5000,
        )

        self.player.setPosition(
            position
        )

    def seek_forward(self):
        duration = self.player.duration()

        position = min(
            duration,
            self.player.position() + 5000,
        )

        self.player.setPosition(
            position
        )

    def set_volume(self, value):
        self.audio_output.setVolume(
            value / 100
        )

        if value == 0:
            self.mute_button.setText(
                "🔇"
            )
        else:
            self.mute_button.setText(
                "🔊"
            )

    def toggle_mute(self):
        muted = self.audio_output.isMuted()

        self.audio_output.setMuted(
            not muted
        )

        if muted:
            self.mute_button.setText(
                "🔊"
            )
        else:
            self.mute_button.setText(
                "🔇"
            )

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.enter_fullscreen()

    def enter_fullscreen(self):
        if self.is_fullscreen:
            return

        self.is_fullscreen = True

        self.header.setParent(None)
        self.time_layout.setParent(None)
        self.controls.setParent(None)
        self.status_label.setParent(None)
        self.position_slider.setParent(None)

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.layout.setSpacing(
            0
        )

        self.fullscreen_button.setText(
            "⛶ 戻す"
        )

        self.showFullScreen()

    def exit_fullscreen(self):
        if not self.is_fullscreen:
            return

        self.is_fullscreen = False

        self.layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        self.layout.setSpacing(
            8
        )

        self.layout.addWidget(
            self.video_widget,
            1,
        )

        self.layout.addLayout(
            self.header
        )

        self.layout.addWidget(
            self.position_slider
        )

        self.layout.addLayout(
            self.time_layout
        )

        self.layout.addLayout(
            self.controls
        )

        self.layout.addWidget(
            self.status_label
        )

        self.fullscreen_button.setText(
            "⛶ 全画面"
        )

        self.showNormal()

        self.raise_()
        self.activateWindow()

    def keyPressEvent(self, event):
        if (
            event.key()
            == Qt.Key.Key_Escape
        ):
            if self.is_fullscreen:
                self.exit_fullscreen()
                event.accept()
                return

        if (
            event.key()
            == Qt.Key.Key_F11
        ):
            self.toggle_fullscreen()
            event.accept()
            return

        super().keyPressEvent(event)

    def _on_position_changed(
        self,
        position,
    ):
        if not self.position_slider.isSliderDown():
            self.position_slider.setValue(
                position
            )

        self.position_label.setText(
            self._format_time(position)
        )

    def _on_duration_changed(
        self,
        duration,
    ):
        self.position_slider.setRange(
            0,
            max(0, duration),
        )

        self.duration_label.setText(
            self._format_time(duration)
        )

    def _on_media_status_changed(
        self,
        status,
    ):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.status_label.setText(
                "動画を読み込みました。"
            )

        elif status == QMediaPlayer.MediaStatus.BufferedMedia:
            self.status_label.setText(
                "再生準備完了"
            )

        elif status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.status_label.setText(
                "再生終了"
            )

        elif status == QMediaPlayer.MediaStatus.InvalidMedia:
            self.status_label.setText(
                "動画を読み込めませんでした。"
            )

    def _on_error(
        self,
        error,
        error_string,
    ):
        if error == QMediaPlayer.Error.NoError:
            return

        message = (
            error_string
            or "動画の再生中にエラーが発生しました。"
        )

        self.status_label.setText(
            f"エラー: {message}"
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

        seconds = (
            total_seconds % 60
        )

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
        if self.is_fullscreen:
            self.exit_fullscreen()

        self.player.stop()

        super().closeEvent(event)