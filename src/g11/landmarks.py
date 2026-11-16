"""Assembly of the (75, 3) landmark vector per frame."""

import numpy as np

POSE_POINTS = 33
HAND_POINTS = 21


class Landmarks:
    """Stack pose and both hands into the model input vector."""

    def stack(self, pose, hands):
        """Join pose and hands into one (75, 3) vector.

        Args:
            pose: Array of shape (33, 3) with the pose landmarks.
            hands: Array of shape (2, 21, 3) with the hand landmarks.

        Returns:
            Array of shape (75, 3): 33 pose, then 21 left, then 21 right
            hand points; a missing hand stays zero.
        """
        return np.concatenate([pose, hands.reshape(2 * HAND_POINTS, 3)])
