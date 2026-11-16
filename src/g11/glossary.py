"""Glossary loading: gloss labels mapped to Spanish words."""

from pathlib import Path

import yaml


class Glossary:
    """Load the glossary YAML for one sign language.

    The glossary is data, not code: gloss labels map to Spanish words
    validated against reference glossaries (GDLSM, FENAS, SIGNA).

    Args:
        path: Path to the glossary YAML file (for example, glossary/LSM.yaml).
    """

    def __init__(self, path):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        self.words = data["words"]
        self.markers = data.get("markers", {})
