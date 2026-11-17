"""Tests for webcam capture with MediaPipe Tasks (hands only, Plan B)."""

import numpy as np

from g11.capture import Capture


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
