"""Tests for the torso-relative normalizer."""

import numpy as np

from g11.normalize import Normalizer


def test_normalize_is_invariant_to_translation():
    rng = np.random.default_rng(1234)
    points = rng.uniform(-1.0, 1.0, size=(32, 75, 3))
    shift = np.array([3.5, -2.0, 0.7])
    normalizer = Normalizer()
    left = normalizer.normalize(points)
    right = normalizer.normalize(points + shift)
    assert np.allclose(left, right, rtol=1e-4, atol=1e-4)
