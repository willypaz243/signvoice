"""Torso-relative normalization of landmark sequences."""

import numpy as np

FRAMES = 32
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6
CLIP = 2.0


class Normalizer:
    """Translate and scale landmark frames to a torso-relative frame.

    The output does not depend on the person's position or distance to
    the camera.
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

    def torso_frame(self, points):
        """Center and scale one frame using the shoulder line.

        Args:
            points: Array of shape (F, 3) with one frame of landmarks.

        Returns:
            Array of shape (F, 3) in the torso frame; zeros when no torso is found.
        """
        left, right = points[LEFT_SHOULDER], points[RIGHT_SHOULDER]
        width = float(np.linalg.norm(left - right))
        if width < 1e-6:
            return np.zeros_like(points)
        center = (left + right) / 2.0
        return np.clip((points - center) / width, -CLIP, CLIP)

    def normalize(self, sequence):
        """Normalize a landmark sequence to the model input shape.

        Args:
            sequence: Array of shape (T, F, 3) with the raw landmarks.

        Returns:
            Array of shape (32, F, 3) in the torso-relative frame.
        """
        sequence = self.to_frames(np.asarray(sequence, dtype=np.float32))
        return np.stack([self.torso_frame(frame) for frame in sequence]).astype(np.float32)
