"""Tests for the glossary loader."""

from pathlib import Path

from g11.glossary import Glossary

ROOT = Path(__file__).resolve().parent.parent


def test_glossary_loads_10_pilot_glosses():
    """The YAML glossary must expose the 10 pilot glosses and the question marker.

    The glossary is data, not code: every gloss label maps to a Spanish
    word (validated against reference glossaries), and the question
    marker is what the phrase template uses to end phrases with "?".
    """
    glossary = Glossary(ROOT / "glossary" / "LSM.yaml")
    assert len(glossary.words) == 10
    assert glossary.words["hola"] == "hola"
    assert "pregunta" in glossary.markers
