import bisect
import threading
import time

import mido


class MIDIPlayer:
    """軽量・時間基準型MIDI再生エンジン。"""

    def __init__(self):
        self.output = None
        self.output_name = None

        # [(秒, [Message, ...]), ...]
        self.events = []
        self.event_times = []

        self.duration = 0.0
        self.position = 0.0

        self.playing = False

        self._thread = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

        self._lock = threading.Lock()

    @staticmethod
    def get_outputs():
        try:
            return list(mido.get_output_names())
        except Exception:
            return []

    def open_output(self, name=None):
        if (
            self.output is not None
            and self.output_name == name
        ):
            return True

        self.close_output()

        outputs = self.get_outputs()

        if not outputs:
            return False

        if name is None:
            name = outputs[0]

        try:
            self.output = mido.open_output(name)
            self.output_name = name
            return True

        except Exception:
            self.output = None
            self.output_name = None
            return False

    def close_output(self):
        self.stop()

        output = self.output

        self.output = None
        self.output_name = None

        if output is not None:
            try:
                output.close()
            except Exception:
                pass

    def load(self, midi_data):
        self.stop()

        self.duration = float(
            midi_data.length
        )

        self.position = 0.0

        grouped = {}

        for note in midi_data.notes:
            grouped.setdefault(
                note.start,
                [],
            ).append(
                mido.Message(
                    "note_on",
                    note=note.note,
                    velocity=note.velocity,
                    channel=note.channel,
                )
            )

            grouped.setdefault(
                note.end,
                [],
            ).append(
                mido.Message(
                    "note_off",
                    note=note.note,
                    velocity=0,
                    channel=note.channel,
                )
            )

        self.events = sorted(
            grouped.items(),
            key=lambda item: item[0],
        )

        self.event_times = [
            event[0]
            for event in self.events
        ]

    def play(self, start_position=None):
        if self.output is None:
            return False

        if not self.events:
            return False

        if start_position is not None:
            with self._lock:
                self.position = max(
                    0.0,
                    min(
                        float(start_position),
                        self.duration,
                    ),
                )

        # 一時停止からの再開
        if (
            self._thread is not None
            and self._thread.is_alive()
        ):
            self._pause_event.clear()
            self.playing = True
            return True

        self._stop_event.clear()
        self._pause_event.clear()
        self.playing = True

        thread = threading.Thread(
            target=self._playback_thread,
            daemon=True,
            name="FileFusion-MIDI",
        )

        self._thread = thread

        thread.start()

        return True

    def pause(self):
        self.playing = False
        self._pause_event.set()

        self._all_notes_off()

    def stop(self):
        self.playing = False

        self._stop_event.set()
        self._pause_event.clear()

        self._all_notes_off()

        with self._lock:
            self.position = 0.0

    def seek(self, position):
        position = max(
            0.0,
            min(
                float(position),
                self.duration,
            ),
        )

        was_playing = self.playing

        self.playing = False
        self._stop_event.set()
        self._pause_event.clear()

        self._all_notes_off()

        with self._lock:
            self.position = position

        if was_playing:
            self._stop_event.clear()
            self.play(position)

    def get_position(self):
        with self._lock:
            return self.position

    def is_available(self):
        return self.output is not None

    def _playback_thread(self):
        """
        絶対時間を基準にして再生します。

        重要:
        「前のイベントを送信してから次を待つ」のではなく、
        再生開始時刻からの絶対時間でイベントを送るため、
        重いMIDIでも処理時間がテンポに累積しません。
        """

        start_position = self.position

        index = bisect.bisect_left(
            self.event_times,
            start_position,
        )

        if index >= len(self.events):
            self.playing = False
            return

        # 実時間上の再生開始点
        wall_start = time.perf_counter()

        while index < len(self.events):

            if self._stop_event.is_set():
                return

            # 一時停止
            while self._pause_event.is_set():

                if self._stop_event.is_set():
                    return

                time.sleep(0.01)

            event_time = (
                self.events[index][0]
            )

            # MIDI上の時間を実時間へ変換
            target_wall_time = (
                wall_start
                + (
                    event_time
                    - start_position
                )
            )

            if not self._wait_until(
                target_wall_time
            ):
                return

            if self._stop_event.is_set():
                return

            output = self.output

            if output is not None:

                try:
                    messages = (
                        self.events[index][1]
                    )

                    for message in messages:
                        output.send(message)

                except Exception:
                    self.playing = False
                    return

            with self._lock:
                self.position = event_time

            index += 1

        with self._lock:
            self.position = self.duration

        self.playing = False

        self._all_notes_off()

    def _wait_until(self, target):
        """
        指定された実時間まで待ちます。

        長時間はsleep。
        最後だけ短く待って精度を確保します。
        """

        while True:

            if self._stop_event.is_set():
                return False

            remaining = (
                target
                - time.perf_counter()
            )

            if remaining <= 0:
                return True

            if remaining > 0.05:
                time.sleep(
                    remaining - 0.02
                )

            elif remaining > 0.01:
                time.sleep(0.005)

            else:
                # 数msだけ細かく待つ
                time.sleep(0)

    def _all_notes_off(self):
        output = self.output

        if output is None:
            return

        for channel in range(16):
            try:
                output.send(
                    mido.Message(
                        "control_change",
                        channel=channel,
                        control=123,
                        value=0,
                    )
                )
            except Exception:
                pass

    def shutdown(self):
        self.close_output()