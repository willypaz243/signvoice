"""Assembly of the (42, 3) hand landmark vector per frame."""

import numpy as np

HAND_POINTS = 21


class Landmarks:
    """Stack both hands into the model input vector.

    Plan B (story 02 spike): pose is dropped because the anonymized
    faces and black clothing keep pose detection near 55 percent, while
    hands reach 90 percent with gamma.
    """

    def stack(self, hands):
        """Join both hands into one (42, 3) vector.

        Args:
            hands: Array of shape (2, 21, 3) with the hand landmarks.

        Returns:
            Array of shape (42, 3): 21 left, then 21 right hand points;
            a missing hand stays zero.
        """
        return np.asarray(hands, dtype=np.float32).reshape(2 * HAND_POINTS, 3)
