"""Tests for the (42, 3) hand landmark vector assembly."""

import numpy as np

from g11.landmarks import Landmarks


def test_landmarks_stack_hands_into_42_vector():
    """Both hands must stack into one (42, 3) vector in order.

    Plan B (story 02 spike): pose is dropped because the anonymized
    faces and black clothing keep pose detection near 55 percent, while
    hands reach 90 percent with gamma. The stack must preserve the hand
    order: left (0:21) then right (21:42).
    """
    hands = np.zeros((2, 21, 3), dtype=np.float32)
    hands[1] = 2.0
    vector = Landmarks().stack(hands)
    assert vector.shape == (42, 3)
    assert np.all(vector[:21] == 0.0)
    assert np.all(vector[21:] == 2.0)
