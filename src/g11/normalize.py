"""Wrist-relative normalization of hand landmark sequences."""

import numpy as np

FRAMES = 32
LEFT = 0
RIGHT = 21
CLIP = 2.0


class Normalizer:
    """Translate and scale hand landmarks to a wrist-relative frame.

    The output does not depend on the signer's position or distance to
    the camera, and a hand the landmarker did not detect stays zero.
    """

    def to_frames(self, sequence):
        """Pad or truncate a sequence to the fixed 32-frame window.

        Args:
            sequence: Array of shape (T, F, 3) with the raw landmarks.

        Returns:
            Array of shape (32, F, 3); short inputs are padded with the last frame.
        """
        frames = sequence.shape[0]
        if frames < FRAMES:
            tail = np.repeat(sequence[-1:], FRAMES - frames, axis=0)
            sequence = np.concatenate([sequence, tail])
        return sequence[:FRAMES]

    def hand_frame(self, points):
        """Center and scale one frame relative to the wrists.

        Args:
            points: Array of shape (42, 3) with both hand landmarks.

        Returns:
            Array of shape (42, 3); a missing hand stays zero.
        """
        present = [i for i in (LEFT, RIGHT) if points[i : i + 21].sum() > 0]
        if present and self._scale(points, present) >= 1e-6:
            return self._centered(points, present)
        return np.zeros_like(points)

    def _centered(self, points, present):
        """Return the wrist-centered, scale-normalized frame."""
        center = np.mean([points[i] for i in present], axis=0)
        scale = self._scale(points, present)
        out = np.zeros_like(points)
        for i in present:
            out[i : i + 21] = np.clip((points[i : i + 21] - center) / scale, -CLIP, CLIP)
        return out

    def _scale(self, points, present):
        """Mean wrist-to-middle-finger distance over the present hands."""
        return float(np.mean([np.linalg.norm(points[i + 9] - points[i]) for i in present]))

    def normalize(self, sequence):
        """Normalize a landmark sequence to the model input shape.

        Args:
            sequence: Array of shape (T, F, 3) with the raw landmarks.

        Returns:
            Array of shape (32, F, 3) in the wrist-relative frame.
        """
        sequence = self.to_frames(np.asarray(sequence, dtype=np.float32))
        return np.stack([self.hand_frame(frame) for frame in sequence]).astype(np.float32)
