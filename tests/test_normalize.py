"""Tests for the wrist-relative hand normalizer."""

import numpy as np

from g11.normalize import Normalizer


def _hand(start, rng):
    """Build one (21, 3) hand with a fixed wrist and palm bone."""
    hand = rng.uniform(0.1, 1.0, size=(21, 3))
    hand[0] = start
    hand[9] = start + np.array([1.0, 0.0, 0.0])
    return hand


def test_normalize_is_invariant_to_translation():
    """Moving the signer in front of the camera must not change the output.

    The normalized landmarks describe the hands relative to the wrist
    line, so adding the same offset to every point (the person stepping
    aside) must produce the same normalized sequence.
    """
    rng = np.random.default_rng(1234)
    frame = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])
    shift = np.array([3.5, -2.0, 0.7])
    normalizer = Normalizer()
    left = normalizer.normalize(frame[None])
    right = normalizer.normalize(frame[None] + shift)
    assert np.allclose(left, right, rtol=1e-4, atol=1e-4)


def test_normalize_is_invariant_to_scale():
    """The distance to the camera must not change the output.

    Doubling every coordinate (hands closer to the camera) must produce
    the same normalized sequence, because the frame is rescaled by the
    wrist-to-middle-finger bone.
    """
    rng = np.random.default_rng(1234)
    frame = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])
    normalizer = Normalizer()
    left = normalizer.normalize(frame[None])
    right = normalizer.normalize(frame[None] * 2.0)
    assert np.allclose(left, right, rtol=1e-4, atol=1e-4)


def test_normalize_keeps_missing_hand_at_zero():
    """A hand that the landmarker did not detect must stay zero.

    The story 02 spike shows hands are missing in some dataset frames;
    the normalizer must not pollute an absent hand with negative center
    values, so the model sees an explicit absence.
    """
    rng = np.random.default_rng(7)
    hands = np.zeros((1, 42, 3), dtype=np.float32)
    hands[0, :21] = _hand([0.0, 0.0, 0.0], rng)
    out = Normalizer().normalize(hands)
    assert np.all(out[:, 21:] == 0.0)
    assert np.abs(out[:, :21]).sum() > 0


def test_normalize_returns_zeros_without_hands():
    """A frame where no hand was detected must normalize to zeros.

    The Espejel images are dark and some frames show no hand at all;
    feeding explicit zeros keeps the sequence shape stable for the GRU.
    """
    hands = np.zeros((1, 42, 3), dtype=np.float32)
    assert np.all(Normalizer().normalize(hands) == 0.0)


def test_normalize_pads_window_to_32_frames():
    """Short clips must be padded to the fixed 32-frame model window.

    The Espejel dataset provides roughly 13 frames per clip, so the
    normalizer has to repeat the last frame until the sequence reaches
    exactly (32, 42, 3) for the model input.
    """
    rng = np.random.default_rng(7)
    frame = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])
    points = np.repeat(frame[None], 10, axis=0)
    assert Normalizer().normalize(points).shape == (32, 42, 3)
