"""Deterministic gloss-to-phrase templates (no invented LSM syntax)."""


class PhraseBuilder:
    """Build a Spanish phrase from gloss labels using glossary words.

    Args:
        words: Mapping of gloss label to Spanish word.
        markers: Mapping of marker gloss to sentence ending (pregunta: ?).
    """

    def __init__(self, words, markers):
        self.words = words
        self.markers = markers

    def build(self, glosses):
        """Join the gloss words and apply the sentence-ending template.

        Args:
            glosses: Ordered list of gloss labels (may include markers).

        Returns:
            The Spanish phrase ending with "." or "?"; an empty string
            when no gloss maps to a word.
        """
        words = [self.words[gloss] for gloss in glosses if gloss in self.words]
        if not words:
            return ""
        text = " ".join(words)
        ending = "?" if any(gloss in self.markers for gloss in glosses) else "."
        return text[0].upper() + text[1:] + ending
