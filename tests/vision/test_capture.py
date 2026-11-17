"""Tests for webcam capture with MediaPipe Tasks (hands only, Plan B)."""

import numpy as np

from vision.capture import Capture


def test_capture_without_camera_detects_from_arrays():
    """Capture must work on plain arrays without opening the webcam.

    The batch scripts (dataset spike, landmark extraction) feed images
    from disk, so the hand landmarker must run with no camera device at
    all.
    """
    capture = Capture(camera=False)
    try:
        ok, frame = capture.frame()
        assert not ok and frame is None
        hands = capture.detect(np.zeros((480, 640, 3), dtype=np.uint8))
        assert hands.shape == (2, 21, 3)
    finally:
        capture.close()


def test_video_mode_detects_hands_over_frames():
    """Video mode must return hand landmarks per frame with timestamps.

    The LSM Glosses ingestion feeds whole videos through the landmarker
    in VIDEO mode (monotonic millisecond timestamps), which keeps track
    of the hands between frames; each call must yield the (2, 21, 3)
    array, with zeros for a frame where no hand is visible.
    """
    capture = Capture(camera=False, video=True)
    try:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        for ms in (0, 33, 67):
            hands = capture.detect_video(frame, ms)
            assert hands.shape == (2, 21, 3)
            assert np.all(hands == 0.0)
    finally:
        capture.close()


def test_capture_detects_hands_for_a_person():
    """The camera must produce hand landmarks for a signer.

    Manual test: run it in front of the webcam with good light. The
    hand array must always have the (2, 21, 3) shape, with zeros for a
    hand the landmarker could not see.
    """
    capture = Capture()
    try:
        ok, frame = capture.frame()
        assert ok
        hands = capture.detect(frame)
        assert hands.shape == (2, 21, 3)
    finally:
        capture.close()
