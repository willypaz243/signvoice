"""Tests for the deterministic gloss-to-phrase templates."""

from pathlib import Path

from g11.glossary import Glossary
from g11.postprocess import PhraseBuilder

ROOT = Path(__file__).resolve().parent.parent


def _builder():
    glossary = Glossary(ROOT / "glossary" / "LSM.yaml")
    return PhraseBuilder(glossary.words, glossary.markers)


def test_postprocess_builds_affirmative_phrase():
    """Gloss labels must become a readable Spanish phrase.

    The template joins the glossary words in order, capitalizes the first
    letter and ends with a period; no LSM syntax is invented, the glosses
    only carry their dictionary words.
    """
    assert _builder().build(["hola", "amigo"]) == "Hola amigo."
