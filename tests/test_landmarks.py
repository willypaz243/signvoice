"""Tests for the (75, 3) landmark vector assembly."""

import numpy as np

from g11.landmarks import Landmarks


def test_landmarks_stack_pose_and_hands_into_75_vector():
    """Pose and both hands must stack into one (75, 3) vector in order.

    The model input is 33 pose points followed by 21 left-hand and
    21 right-hand points; a missing hand stays zero, so the stack must
    preserve the input order exactly.
    """
    pose = np.ones((33, 3), dtype=np.float32)
    hands = np.zeros((2, 21, 3), dtype=np.float32)
    hands[1] = 2.0
    vector = Landmarks().stack(pose, hands)
    assert vector.shape == (75, 3)
    assert np.all(vector[:33] == 1.0)
    assert np.all(vector[33:54] == 0.0)
    assert np.all(vector[54:] == 2.0)
