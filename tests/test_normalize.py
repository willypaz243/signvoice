"""Tests for the torso-relative normalizer."""

import numpy as np

from g11.normalize import Normalizer


def test_normalize_is_invariant_to_translation():
    """Moving the person in front of the camera must not change the output.

    The normalized landmarks describe the sign relative to the torso, so
    adding the same offset to every point (the person stepping closer or
    farther away) must produce the same normalized sequence.
    """
    rng = np.random.default_rng(1234)
    points = rng.uniform(-1.0, 1.0, size=(32, 75, 3))
    shift = np.array([3.5, -2.0, 0.7])
    normalizer = Normalizer()
    left = normalizer.normalize(points)
    right = normalizer.normalize(points + shift)
    assert np.allclose(left, right, rtol=1e-4, atol=1e-4)


def test_normalize_is_invariant_to_scale():
    """The distance to the camera must not change the output.

    Doubling every coordinate (a bigger torso in the frame) must produce
    the same normalized sequence, because the frame is rescaled by the
    shoulder line.
    """
    rng = np.random.default_rng(1234)
    points = rng.uniform(0.5, 1.5, size=(32, 75, 3))
    normalizer = Normalizer()
    left = normalizer.normalize(points)
    right = normalizer.normalize(points * 2.0)
    assert np.allclose(left, right, rtol=1e-4, atol=1e-4)


def test_normalize_pads_window_to_32_frames():
    """Short clips must be padded to the fixed 32-frame model window.

    The Espejel dataset provides roughly 15 frames per word, so the
    normalizer has to repeat the last frame until the sequence reaches
    exactly (32, 75, 3) for the model input.
    """
    rng = np.random.default_rng(7)
    points = rng.uniform(-1.0, 1.0, size=(10, 75, 3))
    normalizer = Normalizer()
    assert normalizer.normalize(points).shape == (32, 75, 3)
