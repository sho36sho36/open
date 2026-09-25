from pathlib import Path

from core.file_detector import FileDetector


def test_extension_detection():
    detector = FileDetector()

    assert detector.get_extension(
        Path("test.MP3")
    ) == ".mp3"


def test_file_info():
    detector = FileDetector()

    info = detector.detect(
        Path("example.mid")
    )

    assert info.extension == ".mid"
    assert info.name == "example.mid"