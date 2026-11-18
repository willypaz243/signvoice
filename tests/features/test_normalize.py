"""Tests for the wrist-relative hand normalizer."""

import numpy as np

from features.normalize import Normalizer


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

    Some video frames show no hand at all; feeding explicit zeros keeps
    the sequence shape stable for the model.
    """
    hands = np.zeros((1, 42, 3), dtype=np.float32)
    assert np.all(Normalizer().normalize(hands) == 0.0)


def test_forward_fill_replaces_zero_frames_with_previous():
    """A frame where no hand was detected must copy the previous frame.

    LSM Glosses videos show both hands in most frames, but a handful of
    frames lose a hand; forward-filling with the last detected frame keeps
    the temporal trajectory smooth instead of jumping to zero, which is the
    preprocessing strategy used by the dataset paper.
    """
    rng = np.random.default_rng(42)
    first = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])[None].astype(
        np.float32
    )
    second = np.concatenate([_hand([0.1, 0.0, 0.0], rng), _hand([5.0, 2.1, 0.0], rng)])[
        None
    ].astype(np.float32)
    sequence = np.concatenate([first, np.zeros_like(first), second], axis=0)
    filled = Normalizer().forward_fill(sequence)
    assert np.array_equal(filled[0], first[0])
    assert np.array_equal(filled[1], first[0])
    assert np.array_equal(filled[2], second[0])


def test_forward_fill_keeps_leading_zeros():
    """Frames before the first detection must stay zero.

    A video can start before the hands enter the frame; there is no
    previous detected frame to copy, so the leading zeros are kept and
    the model sees an explicit absence at the start of the clip.
    """
    rng = np.random.default_rng(42)
    first = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])[None].astype(
        np.float32
    )
    sequence = np.concatenate([np.zeros_like(first), np.zeros_like(first), first], axis=0)
    filled = Normalizer().forward_fill(sequence)
    assert np.all(filled[0] == 0.0)
    assert np.all(filled[1] == 0.0)
    assert np.array_equal(filled[2], first[0])


def test_resample_maps_any_length_to_32_frames():
    """Videos of 31-58 frames must become the fixed 32-frame window.

    Every LSM Glosses video is a little shorter or longer than 32
    frames; the resampler maps the whole video onto the fixed window so
    no clip is cropped to its center.
    """
    rng = np.random.default_rng(7)
    frame = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])[None].astype(
        np.float32
    )
    sequence = np.repeat(frame, 58, axis=0)
    assert Normalizer().resample(sequence).shape == (32, 42, 3)


def test_resample_interpolates_monotone_trajectory():
    """A linear trajectory must stay linear after resampling.

    Resampling is temporal interpolation, not frame picking: if a point
    moves linearly from 0 to 1 across the video, the resampled frame i
    must sit at i/31, exactly where the trajectory is at that instant.
    """
    rng = np.random.default_rng(7)
    base = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)]).astype(
        np.float32
    )
    frames = []
    for t in range(64):
        frame = base.copy()
        frame[0, 0] = t / 63.0
        frames.append(frame)
    sequence = np.stack(frames).astype(np.float32)
    out = Normalizer().resample(sequence)
    assert np.allclose(out[:, 0, 0], np.linspace(0.0, 1.0, 32), atol=1e-3)


def test_resample_of_single_frame_repeats_it():
    """A single detected frame must expand to 32 identical frames.

    A video where the hands are only visible once still has to produce
    a full window; repeating the frame is the only honest option.
    """
    rng = np.random.default_rng(7)
    frame = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])[None].astype(
        np.float32
    )
    out = Normalizer().resample(frame)
    assert out.shape == (32, 42, 3)
    assert np.array_equal(out[0], frame[0])
    assert np.allclose(out, frame[0])


def test_normalize_pads_window_to_32_frames():
    """Short clips must be padded to the fixed 32-frame model window.

    The LSM Glosses clips are short, so the normalizer has to repeat the
    last frame until the sequence reaches exactly (32, 42, 3) for the
    model input.
    """
    rng = np.random.default_rng(7)
    frame = np.concatenate([_hand([0.0, 0.0, 0.0], rng), _hand([5.0, 2.0, 0.0], rng)])
    points = np.repeat(frame[None], 10, axis=0)
    assert Normalizer().normalize(points).shape == (32, 42, 3)
