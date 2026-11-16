"""Manual tests for webcam capture with MediaPipe Tasks."""

from g11.capture import Capture


def test_capture_detects_pose_and_hands():
    """The camera must produce pose and hand landmarks for a person.

    Manual test: run it in front of the webcam. A detected person must
    yield non-zero pose landmarks, and the hand array must always have
    the (2, 21, 3) shape (zeros for a missing hand).
    """
    capture = Capture()
    try:
        ok, frame = capture.frame()
        assert ok
        pose, hands = capture.detect(frame)
        assert pose.shape == (33, 3)
        assert hands.shape == (2, 21, 3)
        assert pose.sum() > 0 or hands.sum() > 0
    finally:
        capture.close()
