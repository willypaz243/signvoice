"""Tests for the one-page demo app."""

from pathlib import Path

from g11.app import DemoApp

ROOT = Path(__file__).resolve().parent.parent


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
