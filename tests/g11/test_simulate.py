"""Tests for the simulated gloss predictor."""

from g11.simulate import SimulatedPredictor


def test_simulate_predicts_deterministically_within_vocabulary():
    """The simulated predictor must be deterministic and stay in the vocabulary.

    The same clip index must always yield the same (gloss, confidence)
    pair, so the demo is reproducible before the real model (story 04)
    replaces it.
    """
    predictor = SimulatedPredictor(["hola", "amigo", "agua"], seed=1234)
    first = predictor.predict(0)
    again = predictor.predict(0)
    assert first == again
    assert first[0] in ["hola", "amigo", "agua"]
    assert 0.0 <= first[1] <= 1.0
