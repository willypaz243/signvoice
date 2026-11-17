"""Tests for the one-page demo app."""

from pathlib import Path

from g11.app import DemoApp, SimulatedPredictor

ROOT = Path(__file__).resolve().parent.parent.parent


def test_app_step_returns_phrase_and_simulated_flag():
    """Every demo step must return a gloss, a phrase and a 'simulado' flag.

    The demo runs before the real model (story 04), so each result has
    to be labelled as simulated and the phrase must follow the
    glossary template for the accumulated glosses.
    """
    demo = DemoApp(ROOT / "glossary" / "LSM.yaml")
    gloss, confidence, phrase, flag = demo.step()
    assert flag == "simulado"
    assert phrase == demo.builder.build([gloss])
    assert 0.0 <= confidence <= 1.0


def test_demo_app_simulated_predictor_still_deterministic():
    """The simulated predictor must stay deterministic after moving into app.

    Story 04 merges simulate.py into app.py (single consumer); the demo
    must keep the same reproducible (gloss, confidence) pairs until the
    live webcam path (story 03) ships.
    """
    assert SimulatedPredictor.__module__ == "g11.app"
    predictor = SimulatedPredictor(["hola", "amigo", "agua"], seed=1234)
    first = predictor.predict(0)
    again = predictor.predict(0)
    assert first == again
    assert first[0] in ["hola", "amigo", "agua"]
    assert 0.0 <= first[1] <= 1.0
