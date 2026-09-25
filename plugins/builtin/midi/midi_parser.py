from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import mido


@dataclass
class MIDINote:
    """MIDIの1音符を表します。"""

    note: int
    start: float
    end: float
    velocity: int
    channel: int
    track: int

    @property
    def duration(self):
        return max(0.0, self.end - self.start)


class MIDIData:
    """解析済みMIDIデータ。"""

    def __init__(self):
        self.filename = ""
        self.ticks_per_beat = 480
        self.length = 0.0
        self.initial_tempo = 500000
        self.tracks = 0
        self.notes = []
        self.channels = set()

    @property
    def note_count(self):
        return len(self.notes)

    @property
    def tempo_bpm(self):
        if self.initial_tempo <= 0:
            return 120.0

        return 60_000_000 / self.initial_tempo


class MIDIParser:
    """MIDIファイルを軽量に解析します。"""

    def parse(self, path):
        path = Path(path)

        midi = mido.MidiFile(str(path))

        data = MIDIData()

        data.filename = path.name
        data.ticks_per_beat = midi.ticks_per_beat
        data.tracks = len(midi.tracks)
        data.length = midi.length

        self._find_initial_tempo(midi, data)
        self._parse_notes(midi, data)

        return data

    def _find_initial_tempo(self, midi, data):
        for track in midi.tracks:
            for message in track:
                if message.type == "set_tempo":
                    data.initial_tempo = message.tempo
                    return

    def _parse_notes(self, midi, data):
        tempo = 500000

        events = []

        for track_index, track in enumerate(midi.tracks):
            absolute_tick = 0

            for order, message in enumerate(track):
                absolute_tick += message.time

                events.append(
                    (
                        absolute_tick,
                        track_index,
                        order,
                        message,
                    )
                )

        events.sort(
            key=lambda item: (
                item[0],
                item[1],
                item[2],
            )
        )

        active_notes = defaultdict(deque)

        current_tick = 0
        current_seconds = 0.0

        for (
            absolute_tick,
            track_index,
            _,
            message,
        ) in events:

            delta_ticks = absolute_tick - current_tick

            if delta_ticks:
                current_seconds += mido.tick2second(
                    delta_ticks,
                    midi.ticks_per_beat,
                    tempo,
                )

            current_tick = absolute_tick

            if message.type == "set_tempo":
                tempo = message.tempo
                continue

            if message.type == "note_on":

                if message.velocity <= 0:
                    self._note_off(
                        active_notes,
                        data,
                        message,
                        current_seconds,
                    )
                    continue

                key = (
                    message.channel,
                    message.note,
                )

                active_notes[key].append(
                    (
                        current_seconds,
                        message.velocity,
                        track_index,
                    )
                )

                data.channels.add(
                    message.channel
                )

            elif message.type == "note_off":
                self._note_off(
                    active_notes,
                    data,
                    message,
                    current_seconds,
                )

        for (
            channel,
            note_number,
        ), note_list in active_notes.items():

            while note_list:
                (
                    start,
                    velocity,
                    track_index,
                ) = note_list.popleft()

                data.notes.append(
                    MIDINote(
                        note=note_number,
                        start=start,
                        end=max(
                            current_seconds,
                            start + 0.05,
                        ),
                        velocity=velocity,
                        channel=channel,
                        track=track_index,
                    )
                )

        data.notes.sort(
            key=lambda note: (
                note.start,
                note.note,
            )
        )

        data.length = max(
            data.length,
            current_seconds,
        )

        if data.notes:
            data.length = max(
                data.length,
                data.notes[-1].end,
            )

    @staticmethod
    def _note_off(
        active_notes,
        data,
        message,
        current_seconds,
    ):
        key = (
            message.channel,
            message.note,
        )

        note_list = active_notes.get(key)

        if not note_list:
            return

        (
            start,
            velocity,
            track_index,
        ) = note_list.popleft()

        if not note_list:
            active_notes.pop(
                key,
                None,
            )

        data.notes.append(
            MIDINote(
                note=message.note,
                start=start,
                end=max(
                    current_seconds,
                    start + 0.001,
                ),
                velocity=velocity,
                channel=message.channel,
                track=track_index,
            )
        )

        data.channels.add(
            message.channel
        )