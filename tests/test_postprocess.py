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


def test_postprocess_builds_question_phrase():
    """The question marker must turn the phrase into a question.

    When the gloss sequence contains the "pregunta" marker, the template
    drops the marker from the words and ends the phrase with "?" instead
    of a period.
    """
    assert _builder().build(["hola", "pregunta"]) == "Hola?"


def test_postprocess_builds_politeness_phrase():
    """A single courtesy gloss must become a complete phrase.

    Short phrases like "gracias" are common in the demo; the template
    must capitalize and close them without adding invented words.
    """
    assert _builder().build(["gracias"]) == "Gracias."
