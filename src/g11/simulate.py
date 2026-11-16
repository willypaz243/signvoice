"""Simulated gloss prediction (the real model arrives in story 04)."""

import numpy as np


class SimulatedPredictor:
    """Pick a gloss deterministically so the demo runs before the real model.

    Args:
        glosses: Vocabulary of gloss labels the predictor may return.
        seed: Base seed; the clip index is added to it for reproducibility.
    """

    def __init__(self, glosses, seed=1234):
        self.glosses = glosses
        self.seed = seed

    def predict(self, clip_index):
        """Return a deterministic (gloss, confidence) pair for a clip.

        Args:
            clip_index: Zero-based index of the clip in the session.

        Returns:
            Tuple (gloss, confidence); the UI marks the result as simulated.
        """
        rng = np.random.default_rng(self.seed + clip_index)
        gloss = self.glosses[int(rng.integers(len(self.glosses)))]
        return gloss, 0.9
